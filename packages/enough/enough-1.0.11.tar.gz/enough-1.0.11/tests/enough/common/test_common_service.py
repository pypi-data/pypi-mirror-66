import os
import pytest
import requests_mock as requests_mock_module
import shutil

from enough import settings
from enough.common import service


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_openstack_create_or_update(tmpdir, openstack_name, requests_mock):
    shutil.copy('infrastructure_key', f'{tmpdir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{tmpdir}/infrastructure_key.pub')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    requests_mock.get(requests_mock_module.ANY, status_code=200)
    domain = f'enough.test'
    s = service.ServiceOpenStack(str(tmpdir), settings.SHARE_DIR, **{
        'driver': 'openstack',
        'playbook': 'tests/enough/common/test_common_service/enough-playbook.yml',
        'domain': domain,
        'name': 'bind',
    })
    s.dotenough.set_certificate('ownca')
    s.dotenough.set_clouds_file('inventory/group_vars/all/clouds.yml')
    r = s.create_or_update()
    assert r['fqdn'] == f'bind.{domain}'
