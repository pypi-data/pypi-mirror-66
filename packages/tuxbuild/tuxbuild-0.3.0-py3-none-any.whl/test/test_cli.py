# -*- coding: utf-8 -*-

import click
from click.testing import CliRunner
import os
import pytest
import tuxbuild.cli

sample_token = "Q9qMlmkjkIuIGmEAw-Mf53i_qoJ8Z2eGYCmrNx16ZLLQGrXAHRiN2ce5DGlAebOmnJFp9Ggcq9l6quZdDTtrkw"
sample_url = "https://foo.bar.tuxbuild.com/v1"


def test_get_config_happy_path(tmp_path):
    """ Test calling get_config with a working config file """
    contents = """
[default]
token={}
api_url={}
""".format(
        sample_token, sample_url
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    c = tuxbuild.cli.get_config(config_path=config_file)
    assert c.get_auth_token() == sample_token
    assert c.get_kbapi_url() == sample_url


def test_get_config_FileNotFoundError(tmp_path):
    """ Test calling get_config with a missing file """
    with pytest.raises(click.exceptions.ClickException):
        tuxbuild.cli.get_config(config_path="/nonexistent")


def test_get_config_PermissionError(tmp_path):
    """ Test calling get_config with an unreadable file """
    contents = """
[default]
token={}
api_url={}
""".format(
        sample_token, sample_url
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    # Make config_file unreadable
    os.chmod(config_file, 0o000)

    uid = os.geteuid()
    if uid == 0:
        # Uh oh, we are running as root
        # Change to some user so that PermissionError will be raised
        os.seteuid(12345)
    with pytest.raises(click.exceptions.ClickException):
        tuxbuild.cli.get_config(config_path=config_file)
    if os.geteuid() != uid:
        # If we changed our uid, change it back
        os.seteuid(uid)


def test_get_config_NoSectionError(tmp_path):
    """ Test calling get_config with no default section """
    contents = """
[XYZ]
token={}
api_url={}
""".format(
        sample_token, sample_url
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    with pytest.raises(click.exceptions.ClickException):
        tuxbuild.cli.get_config(config_path=config_file)


def test_get_config_TokenNotFound(tmp_path):
    """ Test calling get_config with a missing token """
    contents = """
[default]
api_url={}
""".format(
        sample_token, sample_url
    )
    config_file = tmp_path / "config.ini"
    config_file.write_text(contents)
    with pytest.raises(click.exceptions.ClickException):
        tuxbuild.cli.get_config(config_path=config_file)


def test_get_auth_token(config_valid_token):
    token = tuxbuild.cli.get_auth_token(config_valid_token)
    assert isinstance(token, str)


def test_get_auth_token_invalid(config_invalid_token):
    with pytest.raises(click.ClickException):
        tuxbuild.cli.get_auth_token(config_invalid_token)


def test_usage():
    """ Test running cli() with no arguments """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.cli, [])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "Commands" in result.output


def test_build_no_args():
    """ Test calling build() with no options """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.build, [])
    assert result.exit_code == 2
    assert "Usage" in result.output
    assert "help" in result.output


def test_build_usage():
    """ Test calling build() with --help """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.build, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "--toolchain" in result.output
    assert "--git-repo TEXT" in result.output


@pytest.fixture
def tuxbuild_config(tmp_path, monkeypatch):
    c = tmp_path / "config.ini"
    with c.open("w") as f:
        f.write("[default]\n")
        f.write(f"token={sample_token}\n")
        f.write(f"api_url={sample_url}\n")
    monkeypatch.setenv("TUXBUILD_CONFIG", str(c))
    return c


def test_build(mocker, tuxbuild_config):
    build = mocker.patch("tuxbuild.build.Build.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1


def test_build_quiet(mocker, tuxbuild_config):
    Build = mocker.patch("tuxbuild.build.Build")
    Build.return_value.build_data = "https://tuxbuild.example.com/abcdef0123456789"
    mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--quiet",
        ],
    )
    assert result.exit_code == 0
    assert "Building Linux Kernel" not in result.output
    assert result.output == "https://tuxbuild.example.com/abcdef0123456789\n"


sample_build_set = """
sets:
  - name: test
    builds:
      - {target_arch: arm64, toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: arm, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: clang-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: i386, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: riscv, toolchain: gcc-9, kconfig: allyesconfig}
"""


def test_build_set(mocker, tmp_path, tuxbuild_config):
    build = mocker.patch("tuxbuild.build.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    config = tmp_path / "buildset.yaml"
    with config.open("w") as f:
        f.write(sample_build_set)
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={config}",
            "--set-name=test",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 9


def test_build_set_quiet(mocker, tmp_path, tuxbuild_config):
    BuildSet = mocker.patch("tuxbuild.build.BuildSet")
    builds = []
    for i in range(1, 10):
        build = mocker.MagicMock()
        build.build_data = f"https://tuxbuild.example.com/{i}"
        builds.append(build)
    BuildSet.return_value.build_objects = builds
    mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    config = tmp_path / "buildset.yaml"
    with config.open("w") as f:
        f.write(sample_build_set)
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={config}",
            "--set-name=test",
            "--quiet",
        ],
    )
    assert result.exit_code == 0
    output = "".join([f"https://tuxbuild.example.com/{i}\n" for i in range(1, 10)])
    assert result.output == output
