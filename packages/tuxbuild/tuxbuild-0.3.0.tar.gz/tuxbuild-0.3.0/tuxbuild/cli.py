# -*- coding: utf-8 -*-

import click
import concurrent.futures
import configparser
import json
import sys
import time
import tuxbuild.build
import tuxbuild.config
import tuxbuild.exceptions
import yaml
import requests
import re
from os.path import expanduser


info = click.echo


def error(msg):
    raise click.ClickException(msg)


def warning(msg):
    click.echo(msg, err=True)


def no_info(_):
    pass


def quiet_output(quiet):
    global info
    if quiet:
        info = no_info


def get_config(config_path="~/.config/tuxbuild/config.ini"):
    try:
        return tuxbuild.config.Config(config_path)
    except (
        FileNotFoundError,
        PermissionError,
        configparser.NoSectionError,
        tuxbuild.exceptions.TokenNotFound,
    ) as e:
        error(e)


def get_auth_token(config):
    try:
        config.check_auth_token()
        return config.get_auth_token()
    except Exception as e:
        print(e)
        error("😔 Invalid Token")


def get_default_buildset():
    home = expanduser("~")
    return "{}/.config/tuxbuild/builds.yaml".format(home)


def wait_for_state_change(build_object, state_items):
    for item in state_items:
        info(item.get("message") + str(build_object))
        try:
            build_object.wait_on_status(item.get("state"))
        except tuxbuild.exceptions.Timeout as e:
            warning(
                click.style(
                    "🔧 Tuxbuild Error ({}): Please resubmit this build", fg="white"
                ).format(str(e))
                + str(build_object)
            )
            return False
    return True


def wait_for_object(build_object):
    """ Wait for a build to complete. Return True if the build completed successfully """
    state_items = [
        {
            "state": "queued",
            "message": click.style("⏳ Queued: ", fg="white", bold=True),
        },
        {
            "state": "building",
            "message": click.style("⚗️  Building: ", fg="cyan", bold=True),
        },
    ]
    if not wait_for_state_change(build_object, state_items):
        return False
    # Check for build result
    elif build_object.tuxbuild_status != "complete":
        status_message = build_object.status_message
        warning(
            click.style("🔧 Tuxbuild Error ({}): ", fg="white").format(status_message)
            + str(build_object)
        )
        return False
    elif build_object.build_status == "fail":
        status_message = build_object.status_message
        errors_count = build_object.errors_count
        error_message = ""
        if errors_count == 1:
            error_message = f"({errors_count} error)"
        if errors_count > 1:
            error_message = f"({errors_count} errors)"
        if status_message:
            error_message += f" with status message '{status_message}'"
        warning(
            click.style("👹 Fail {}: ", fg="bright_red", bold=True).format(error_message)
            + str(build_object)
        )
        return False
    elif build_object.build_status == "pass":
        warnings_count = build_object.warnings_count
        if warnings_count == 0:
            info(
                click.style(
                    "🎉 Pass ({} warnings): ".format(warnings_count),
                    fg="green",
                    bold=True,
                )
                + str(build_object)
            )
        elif warnings_count == 1:
            warning(
                click.style(
                    "👾 Pass ({} warning): ".format(warnings_count),
                    fg="yellow",
                    bold=True,
                )
                + str(build_object)
            )
        else:
            warning(
                click.style(
                    "👾 Pass ({} warnings): ".format(warnings_count),
                    fg="yellow",
                    bold=True,
                )
                + str(build_object)
            )
        return True
    return False


@click.group()
@click.version_option()  # Implement --version
def cli():
    pass


@cli.command()
@click.option("--git-repo", required=True, help="Git repository")
@click.option("--git-ref", required=True, help="Git reference")
@click.option(
    "--target-arch",
    required=True,
    help="Target architecture [arm64|arm|x86|i386|mips|arc|riscv]",
)
@click.option(
    "--kconfig",
    required=True,
    multiple=True,
    help="Kernel kconfig arguments (may be specified multiple times)",
)
@click.option(
    "--toolchain", required=True, help="Toolchain [gcc-8|gcc-9|clang-8|clang-9]"
)
@click.option(
    "--kconfig-allconfig",
    required=False,
    help=(
        "Argument used only with allyesconfig/allmodconfig/allnoconfig/randconfig."
        "The argument is a path to a file with specific config symbols which you want to override"
    ),
)
@click.option(
    "--json-out",
    required=False,
    help="Write json build status out to a named file path",
    type=click.File("w", encoding="utf-8"),
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Supress all informational output; prints only the download URL for the build",
)
def build(
    git_repo,
    git_ref,
    target_arch,
    kconfig,
    toolchain,
    kconfig_allconfig=None,
    json_out=None,
    quiet=False,
):
    quiet_output(quiet)

    auth = get_config()
    token = get_auth_token(auth)
    kbapi_url = auth.get_kbapi_url()
    build = tuxbuild.build.Build(
        git_repo=git_repo,
        git_ref=git_ref,
        target_arch=target_arch,
        kconfig=kconfig,
        toolchain=toolchain,
        token=token,
        kbapi_url=kbapi_url,
        kconfig_allconfig=kconfig_allconfig,
    )
    info("Building Linux Kernel {} at {}".format(git_repo, git_ref))
    try:
        build.build()
    except tuxbuild.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))
    build_result = wait_for_object(build)
    if json_out:
        json_out.write(json.dumps(build.status, sort_keys=True, indent=4))
    if quiet:
        print(build.build_data)
    if not build_result:
        sys.exit(1)


def get_tux_config(url, retries=3, sleep=3):
    result = requests.get(url)
    if result.status_code != 200:
        if retries == 0:
            raise tuxbuild.exceptions.TuxbuildError(
                f"Unable to retrieve {url}: {result.reason}"
            )
        time.sleep(sleep)
        return get_tux_config(url, retries - 1, sleep * 2)
    return result.text


@cli.command()
@click.option(
    "--tux-config",
    default=get_default_buildset(),
    help="Path or a web URL to tuxbuild config file",
)
@click.option("--set-name", required=True, help="Set name")
@click.option("--git-repo", required=True, help="Git repository")
@click.option("--git-ref", required=True, help="Git reference")
@click.option(
    "--target-arch",
    required=False,
    help="Target architecture [arm64|arm|x86|i386|mips|arc|riscv]",
)
@click.option(
    "--kconfig",
    required=False,
    multiple=True,
    help="Kernel kconfig arguments (may be specified multiple times)",
)
@click.option(
    "--toolchain", required=False, help="Toolchain [gcc-8|gcc-9|clang-8|clang-9]"
)
@click.option(
    "--kconfig-allconfig",
    required=False,
    help=(
        "Argument used only with allyesconfig/allmodconfig/allnoconfig/randconfig."
        "The argument is a path to a file with specific config symbols which you want to override"
    ),
)
@click.option(
    "--json-out",
    required=False,
    help="Write json build status out to a named file path",
    type=click.File("w", encoding="utf-8"),
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Supress all informational output; prints only the download URLs for the builds",
)
def build_set(
    tux_config,
    set_name,
    git_repo=None,
    git_ref=None,
    target_arch=None,
    kconfig=(),
    kconfig_allconfig=None,
    toolchain=None,
    json_out=None,
    quiet=None,
):
    quiet_output(quiet)

    params = {}
    params["git_repo"] = git_repo
    params["git_ref"] = git_ref
    params["target_arch"] = target_arch
    params["kconfig"] = kconfig
    params["kconfig_allconfig"] = kconfig_allconfig
    params["toolchain"] = toolchain
    config = get_config()
    token = get_auth_token(config)
    kbapi_url = config.get_kbapi_url()
    tux_config_regex = re.compile(r"^https?://")
    if tux_config_regex.match(tux_config):
        tux_config_contents = yaml.safe_load(get_tux_config(tux_config))
    else:
        with open(tux_config, "r") as f:
            tux_config_contents = yaml.safe_load(f)

    info("Building Linux Kernel build set {}".format(set_name))
    # Find build named set_name
    build_list = None
    for bs in tux_config_contents.get("sets"):
        if bs.get("name") == set_name:
            build_list = bs.get("builds")
            assert (
                len(build_list) > 0
            ), "build set {} does not contain any builds".format(set_name)
            break

    # Build not found in config
    if not build_list:
        error("No set named {} found in {}".format(set_name, tux_config))

    # Create build objects. Do this first to take advantage of argument validation
    # before submitting builds
    build_objects = []
    for b in build_list:
        for param in ["git_repo", "git_ref", "target_arch", "kconfig", "toolchain"]:
            if params[param]:
                b[param] = params[param]
            elif param not in b:
                error(
                    "No {} found in command line or in the set {} in {}: {}".format(
                        param, set_name, tux_config, b
                    )
                )

        # kconfig_allconfig is optional api parameter hence it may not be defined
        # in cli or the set. We need to explicitly set it to None
        if params.get("kconfig_allconfig") is not None:
            b["kconfig_allconfig"] = params.get("kconfig_allconfig")
        elif "kconfig_allconfig" not in b:
            b["kconfig_allconfig"] = None

        build_objects.append(
            tuxbuild.build.Build(
                git_repo=b["git_repo"],
                git_ref=b["git_ref"],
                target_arch=b["target_arch"],
                kconfig=b["kconfig"],
                toolchain=b["toolchain"],
                token=token,
                kbapi_url=kbapi_url,
                kconfig_allconfig=b["kconfig_allconfig"],
            )
        )

    build_set = tuxbuild.build.BuildSet(build_objects, token, kbapi_url)

    try:
        build_set.build()
    except tuxbuild.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    # Wait for the builds to complete - one watcher thread per build
    # Gather the results in build_results
    build_results = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(build_objects)
    ) as executor:
        for b in build_objects:
            build_results.append(executor.submit(wait_for_object, b))

    if json_out:
        json_out.write(json.dumps(build_set.status_list, sort_keys=True, indent=4))

    if quiet:
        for build in build_set.build_objects:
            print(build.build_data)

    # If any of the builds did not pass, exit with exit code of 1
    if False in [result._result for result in build_results]:
        sys.exit(1)
