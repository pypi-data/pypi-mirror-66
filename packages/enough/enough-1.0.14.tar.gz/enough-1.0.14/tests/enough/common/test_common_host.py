from enough.common.host import HostDocker
from enough.common import tcp
from enough import settings


def test_docker_create_or_update(tmpdir, docker_name, tcp_port):
    host = HostDocker(str(tmpdir), settings.SHARE_DIR, **{
        'name': docker_name,
        'domain': docker_name,
        'port': tcp_port,
    })
    host.create_or_update()
    assert '"Status":"healthy"' in host.d.get_logs()
    host.d.down()


def test_docker_create_or_update_same_network(tmpdir, docker_name):
    name1 = f'{docker_name}1'
    port1 = tcp.free_port()
    host1 = HostDocker(f'{tmpdir}/1', settings.SHARE_DIR, **{
        'name': name1,
        'domain': docker_name,
        'port': port1,
    })
    host1.create_or_update()
    assert '"Status":"healthy"' in host1.d.get_logs()

    name2 = f'{docker_name}2'
    port2 = tcp.free_port()
    host2 = HostDocker(f'{tmpdir}/2', settings.SHARE_DIR, **{
        'name': name2,
        'domain': docker_name,
        'port': port2,
    })
    host2.create_or_update()
    assert '"Status":"healthy"' in host2.d.get_logs()

    assert host2.d.docker_compose.exec('-T', name2, 'ping', '-c1', name1)


def test_docker_delete(tmpdir, docker_name, tcp_port):
    domain = f'{docker_name}.domain'
    host = HostDocker(str(tmpdir), settings.SHARE_DIR, **{
        'name': docker_name,
        'domain': domain,
        'port': tcp_port,
    })

    def count():
        r = host.d.docker.ps('-q', '--format=json', '--filter', f'label=enough={domain}')
        o = r.stdout.strip().decode('utf8')
        if o:
            return len(o.split('\n'))
        else:
            return 0

    assert count() == 0
    host.create_or_update()
    assert '"Status":"healthy"' in host.d.get_logs()
    assert count() == 1

    related_container = f'extra_{docker_name}'
    host.d.docker.run('--name', related_container,
                      '--label', f'enough={domain}',
                      '--detach',
                      'debian:buster', 'sleep', '3600')
    assert count() == 2
    host.delete()
    assert count() == 0
