from abc import ABC, abstractmethod
import logging
import re
import requests

from enough import settings
from enough.common import openstack
from enough.common import dotenough
from enough.common import ansible_utils

log = logging.getLogger(__name__)


class Service(ABC):

    def __init__(self, config_dir, share_dir):
        self.config_dir = config_dir
        self.share_dir = share_dir

        self.service2hosts = {}

        bind = ['bind-host', 'icinga-host', 'postfix-host', 'wazuh-host']
        self.service2hosts['bind'] = bind
        self.service2hosts['cloud'] = bind[:] + ['cloud-host']

    @abstractmethod
    def create_or_update(self):
        pass


class ServiceDocker(Service):
    pass


class ServiceOpenStack(Service):

    class PingException(Exception):
        pass

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def maybe_delegate_dns(self):
        subdomain_regexp = r'(.*)\.d\.(.*)'
        m = re.match(subdomain_regexp, self.args['domain'])
        if not m:
            log.info(f'{self.args["domain"]} does not match "{subdomain_regexp}", '
                     'do not attempt to delegate the DNS')
            return False
        (subdomain, domain) = m.group(1, 2)
        api = f'api.{domain}'
        ping = f'https://{api}/ping/'
        r = requests.get(ping)
        if not r.ok:
            raise ServiceOpenStack.PingException(f'{ping} does not respond')

        h = openstack.Heat(self.config_dir, self.dotenough.clouds_file)
        s = openstack.Stack(self.config_dir,
                            self.dotenough.clouds_file,
                            h.get_stack_definition('bind-host'))
        s.set_public_key(self.dotenough.public_key())
        bind_host = s.create_or_update()
        r = requests.post(f'https://{api}/delegate-dns/',
                          json={
                              'name': subdomain,
                              'ip': bind_host['ipv4'],
                          })
        r.raise_for_status()
        return True

    def create_or_update(self):
        self.maybe_delegate_dns()
        hosts = self.service2hosts[self.args['name']]
        h = openstack.Heat(self.config_dir, self.dotenough.clouds_file)
        h.create_or_update(hosts, self.dotenough.public_key())
        h.write_inventory()
        playbook = ansible_utils.Playbook(self.config_dir, self.share_dir)
        playbook.run([
            f'--private-key={self.dotenough.private_key()}',
            '--limit', ','.join(hosts + ['localhost']),
            f'{self.share_dir}/{self.args["playbook"]}',
        ])
        return {'fqdn': f'{self.args["name"]}.{self.args["domain"]}'}


def service_factory(**kwargs):
    if kwargs['driver'] == 'openstack':
        return ServiceOpenStack(settings.CONFIG_DIR, settings.SHARE_DIR, **kwargs)
    else:
        return ServiceDocker(settings.CONFIG_DIR, settings.SHARE_DIR, **kwargs)
