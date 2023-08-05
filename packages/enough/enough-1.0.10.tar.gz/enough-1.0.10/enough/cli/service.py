from cliff.show import ShowOne

from enough.common.service import service_factory


def set_common_options(parser):
    parser.add_argument('--driver', default='openstack')
    return parser


class Create(ShowOne):
    "Create or update a service"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        parser.add_argument('--playbook', default='enough-playbook.yml')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        service = service_factory(**args)
        r = service.create_or_update()
        columns = ('name',)
        data = (r['fqdn'],)
        return (columns, data)
