from django.conf import settings
from enough.common import bind, openstack
import os

from enough.common import ansible_utils
from enough.common import dotenough


class Hosting(dotenough.DotEnoughOpenStack):

    def __init__(self, name):
        super().__init__(settings.CONFIG_DIR, f"{name}.d.{settings.ENOUGH_DOMAIN}")
        self.name = name

    def create_hosts(self, public_key):
        names = ('bind-host', 'icinga-host', 'postfix-host', 'wazuh-host')
        h = openstack.Heat(self.config_dir, self.clouds_file)
        inventory = h.to_inventory(h.create_or_update(names, public_key))
        self.populate_hosts_file(inventory)
        return names

    def populate_config(self):
        if os.path.exists('/etc/ssl/certs/fakelerootx1.pem'):
            certificate_authority = 'letsencrypt_staging'
        else:
            certificate_authority = 'letsencrypt'
        return super().populate_config(certificate_authority)

    def create_or_update(self):
        o = openstack.OpenStack(self.config_dir, self.clouds_file)
        assert o.allocate_cloud(
            f'{self.config_dir}/api/hosting/all', self.clouds_file)
        s = openstack.Stack(self.clouds_file,
                            openstack.Heat.get_stack_definition('bind-host'))
        key = self.ensure_ssh_key()
        s.set_public_key(f'{key}.pub')
        bind_host = s.create_or_update()
        bind.delegate_dns(f'd.{settings.ENOUGH_DOMAIN}', self.name, bind_host['ipv4'])
        names = self.create_hosts(f'{key}.pub')
        self.populate_config()
        ansible_utils.bake_ansible_playbook()(
            '-i', f'{self.config_dir}/inventory',
            '--private-key', key,
            '--limit', ','.join(names + ('localhost',)),
            'playbook.yml')

    def delete(self):
        names = ('bind-host', 'icinga-host', 'postfix-host', 'wazuh-host')
        for name in names:
            s = openstack.Stack(self.clouds_file,
                                openstack.Heat.get_stack_definition(name))
            s.delete()
        return {}
