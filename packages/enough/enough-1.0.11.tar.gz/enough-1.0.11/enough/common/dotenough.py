import textwrap
import os
import re
import sh
import shutil
import yaml


class DotEnough(object):

    def __init__(self, config_dir, domain):
        self.domain = domain
        self.config_dir = config_dir
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

    def ensure(self):
        self.ensure_ssh_key()

    def ensure_ssh_key(self):
        path = f'{self.config_dir}/infrastructure_key'
        if not os.path.exists(path):
            sh.ssh_keygen('-f', path, '-N', '', '-b', '4096', '-t', 'rsa')
        return path

    def public_key(self):
        return f'{self.ensure_ssh_key()}.pub'

    def private_key(self):
        return self.ensure_ssh_key()

    def populate_hosts_file(self, inventory):
        d = f'{self.config_dir}/inventory'
        if not os.path.exists(d):
            os.makedirs(d)
        open(f'{d}/hosts.yml', 'w').write(inventory)

    def populate_config(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

        if not os.path.exists(f'{d}/private-key.yml'):
            open(f'{d}/private-key.yml', 'w').write(textwrap.dedent(f"""\
            ---
            ssh_private_keyfile: {self.config_dir}/infrastructure_key
            """))

        if not os.path.exists(f'{d}/domain.yml'):
            open(f'{d}/domain.yml', 'w').write(textwrap.dedent(f"""\
            ---
            domain: {self.domain}
            production_domain: {self.domain}
            """))

        if not os.path.exists(f'{d}/certificate.yml'):
            self.set_certificate(certificate_authority)

    def set_certificate(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        open(f'{d}/certificate.yml', 'w').write(textwrap.dedent(f"""\
        ---
        certificate_authority: {certificate_authority}
        """))

    @staticmethod
    def remap(argv):
        home = os.path.expanduser('~/.enough')

        def remap(s):
            s = re.sub(r'^/\S+/.enough', home, s)
            s = re.sub(r'=/\S+/.enough', f'={home}', s)
            return s
        return [remap(a) for a in argv]

    @staticmethod
    def preserve_ownership():
        uid = os.geteuid()
        home = os.path.expanduser('~/.enough')
        if not uid == 0 or not os.path.exists(home):
            return False
        home_uid = os.stat(home).st_uid
        if uid != home_uid:
            os.system(f'chown -R {home_uid} {home}')
        return True


class DotEnoughOpenStack(DotEnough):

    def __init__(self, config_dir, domain):
        super().__init__(config_dir, domain)
        self.clouds_file = f'{self.config_dir}/inventory/group_vars/all/clouds.yml'

    def set_clouds_file(self, clouds_file):
        shutil.copy(clouds_file, self.clouds_file)

    def ensure(self):
        super().ensure()
        self.populate_config('letsencrypt')
        self.set_missing_config_file_from_openrc(f'{self.config_dir}/openrc.sh', self.clouds_file)

    @staticmethod
    def set_missing_config_file_from_openrc(openrc, config_file):
        if os.path.exists(openrc) and not os.path.exists(config_file):
            DotEnoughOpenStack.openrc2clouds(openrc, config_file)
            return True
        else:
            return False

    @staticmethod
    def openrc2clouds(openrc, clouds):
        c = {
            'auth': {
                'user_domain_name': 'Default',
                'password': 'PLACEHOLDER',
            }
        }
        for line in open(openrc).readlines():
            r = re.search(r'export\s+(OS_\w+)="(.*)"', line)
            if not r:
                r = re.search(r'export\s+(OS_\w+)=(.*)\s*', line)
                if not r:
                    continue
            (k, v) = r.group(1, 2)
            if k == 'OS_REGION_NAME':
                c['region_name'] = v
            elif k == 'OS_AUTH_URL':
                c['auth']['auth_url'] = v
            elif k == 'OS_PROJECT_NAME' or k == 'OS_TENANT_NAME':
                c['auth']['project_name'] = v
            elif k == 'OS_PROJECT_ID' or k == 'OS_TENANT_ID':
                c['auth']['project_id'] = v
            elif k == 'OS_USERNAME':
                c['auth']['username'] = v
            elif k == 'OS_PASSWORD' and v != '$OS_PASSWORD_INPUT':
                c['auth']['password'] = v
        open(clouds, 'w').write(yaml.dump({
            'clouds': {
                'ovh': c
            }
        }))
        return c


class DotEnoughDocker(DotEnough):

    def ensure(self):
        super().ensure()
        self.populate_config('ownca')
