import os
from abc import ABC, abstractmethod
import shutil
import tempfile

from enough import settings
from enough.common import openstack
from enough.common import docker
from enough.common import dotenough
from enough.common import tcp


class Host(ABC):

    def __init__(self, config_dir, share_dir):
        self.config_dir = config_dir
        self.share_dir = share_dir

    @abstractmethod
    def create_or_update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def write_inventory(self):
        pass


class HostDocker(Host):

    class DockerInfrastructure(docker.Docker):

        def __init__(self, config_dir, **kwargs):
            self.config_dir = config_dir
            super().__init__(**kwargs)

        def create_image(self):
            name = super().create_image()
            dockerfile = os.path.join(self.root, 'internal/data/infrastructure.dockerfile')
            with tempfile.TemporaryDirectory() as d:
                shutil.copy(f'{self.config_dir}/infrastructure_key.pub', d)
                return self._create_image(None,
                                          '--build-arg', f'IMAGE_NAME={name}',
                                          '-f', dockerfile, d)

        def get_compose_content(self):
            f = os.path.join(self.root, 'internal/data/infrastructure-docker-compose.yml')
            return self.replace_content(open(f).read())

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughDocker(config_dir, self.args['domain'])
        self.dotenough.ensure()
        self.d = HostDocker.DockerInfrastructure(config_dir, **self.args)

    def create_or_update(self):
        self.d.create_network(self.args['domain'])
        self.d.name = self.args['name']
        port = self.d.get_public_port('22')
        if not port:
            port = tcp.free_port()
            self.args['port'] = port
            self.d = HostDocker.DockerInfrastructure(self.config_dir, **self.args)
            self.d.create_or_update()
        return {
            'ipv4': self.d.get_ip(),
            'port': '22',
        }

    def delete(self):
        domain = self.args['domain']
        for id in self.d.docker.ps('--filter', f'label=enough={domain}', '-q', _iter=True):
            self.d.docker.rm('-f', id.strip())

    def write_inventory(self):
        pass


class HostOpenStack(Host):

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def create_or_update(self):
        h = openstack.Heat(self.config_dir, self.args['clouds'])
        s = openstack.Stack(self.config_dir,
                            self.args['clouds'],
                            h.get_stack_definition(self.args['name']))
        s.set_public_key(f'{self.config_dir}/infrastructure_key.pub')
        return s.create_or_update()

    def delete(self):
        h = openstack.Heat(self.config_dir, self.args['clouds'])
        for name in self.args['name']:
            s = openstack.Stack(self.config_dir,
                                self.args['clouds'],
                                h.get_stack_definition(name))
            s.delete()

    def write_inventory(self):
        openstack.Heat(self.config_dir, self.args['clouds']).write_inventory()


def host_factory(**kwargs):
    if kwargs['driver'] == 'openstack':
        return HostOpenStack(settings.CONFIG_DIR, settings.SHARE_DIR, **kwargs)
    else:
        return HostDocker(settings.CONFIG_DIR, settings.SHARE_DIR, **kwargs)
