import argparse
from enough.cli import host


def test_set_common_options():
    parser = argparse.ArgumentParser()
    assert host.set_common_options(parser) == parser
    args = parser.parse_args([])
    assert '/inventory/' in args.clouds
    driver = 'DRIVER'
    clouds = 'CLOUDS'
    args = parser.parse_args(['--driver', driver, '--clouds', clouds])
    assert args.clouds == clouds
    assert args.driver == driver
