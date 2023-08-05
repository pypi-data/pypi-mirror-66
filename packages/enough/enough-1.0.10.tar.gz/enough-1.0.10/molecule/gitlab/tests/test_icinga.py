from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['icinga-host']


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'gitlab-host')
        assert r['attrs']['name'] == 'gitlab-host'

    def test_service(self, host):
        assert self.is_service_ok('gitlab-host!Gitlab')
