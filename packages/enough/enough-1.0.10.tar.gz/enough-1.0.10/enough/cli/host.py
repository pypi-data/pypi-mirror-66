from cliff.show import ShowOne
from cliff.command import Command

from enough import settings
from enough.common.host import host_factory


def set_common_options(parser):
    parser.add_argument('--driver', default='openstack')
    openstack = parser.add_argument_group(title='OpenStack',
                                          description='Only when --driver=openstack')
    openstack.add_argument(
        '--clouds',
        default=f'{settings.CONFIG_DIR}/inventory/group_vars/all/clouds.yml',
        help='Path to the clouds.yml file')
    return parser


class Create(ShowOne):
    "Create or update a host"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        host = host_factory(**args)
        r = host.create_or_update()
        columns = ('name', 'user', 'port', 'ip')
        data = (parsed_args.name, 'debian', r['port'], r['ipv4'])
        return (columns, data)


class Delete(Command):
    "Delete a host"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', nargs='+')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        host = host_factory(**args)
        host.delete()


class Inventory(Command):
    "Write an ansible compatible inventory of all hosts"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        host = host_factory(**args)
        host.write_inventory()
