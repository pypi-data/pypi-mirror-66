###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import print_function

import argparse
from collections import defaultdict
from datetime import datetime
import logging
import pipes
import os
from os.path import basename, isdir, join, relpath
import re
import sys
import tempfile

INSTALL_ROOT = "/cvmfs/lhcbdev.cern.ch/conda"
ENVS_ROOT = join(INSTALL_ROOT, "envs")
CONDA_CMD = join(INSTALL_ROOT, "miniconda/linux-64/prod/bin/conda")
LHCB_ETC = "/cvmfs/lhcb.cern.ch/etc/grid-security"
ENV_VAR_WHITELIST = [
    # General unix
    r"DISPLAY",
    r"EDITOR",
    r"HOME",
    r"HOSTNAME",
    r"LANG",
    r"LC_.*",
    r"TMPDIR",
    r"TZ",
    r"USER",
    r"VISUAL",
    # HEP specific
    r"VOMS_.*",
    r"X509_.*",
    r"XRD_.*",
    # LHCb specific
    r"MYSITEROOT",
]
ENV_VAR_WHITELIST = re.compile(r"^(" + r"|".join(ENV_VAR_WHITELIST) + r")$")

logging.getLogger().setLevel(logging.INFO)


def list_environments(subdir="linux-64"):
    envs = defaultdict(dict)
    for dirpath, dirnames, filenames in os.walk(ENVS_ROOT, topdown=True):
        if subdir in dirnames:
            split_dirpath = relpath(dirpath, ENVS_ROOT).split(os.sep)
            if len(split_dirpath) < 2:
                sys.stderr.write("ERROR: Invalid environment found (%s)" % dirpath)
                sys.stderr.flush()
                continue
            env_name = "/".join(split_dirpath[:-1])
            env_version = split_dirpath[-1]
            envs[env_name][env_version] = join(dirpath, subdir)
            # Avoid searching any deeper in the tree
            dirnames[:] = []

    # Add the short versions with YYYY-MM-DD instead of YYYY-MM-DD_HH-MM
    display_versions = defaultdict(list)
    for env in envs:
        versions = defaultdict(list)
        for long_version, env_path in sorted(envs[env].items()):
            short_version = datetime.strptime(long_version, "%Y-%m-%d_%H-%M").strftime(
                "%Y-%m-%d"
            )
            envs[env][short_version] = env_path
            versions[short_version].append(long_version)

        for short_version, long_versions in versions.items():
            if len(long_versions) == 1:
                display_versions[env].append(short_version)
            else:
                display_versions[env].extend(long_versions)

    return envs, display_versions


CONDA_ENVIRONMENTS, DISPLAY_VERSIONS = list_environments()


def call_in_conda(command, env_name, env_version):
    """Replace the current process with a command in the conda environment

    If the command is successfully executed this function will never return.
    """
    env_prefix = CONDA_ENVIRONMENTS[env_name][env_version]

    env = {k: v for k, v in os.environ.items() if ENV_VAR_WHITELIST.match(k)}
    with tempfile.NamedTemporaryFile(mode="wt", delete=False) as bashrc:
        logging.debug("Writing bashrc to %s", bashrc.name)
        bashrc.write(
            "\n".join(
                [
                    'eval "$({} shell.bash hook)"'.format(pipes.quote(CONDA_CMD)),
                    "conda activate {}".format(pipes.quote(env_prefix)),
                    "unset BASH_ENV",
                    "rm {}".format(pipes.quote(bashrc.name)),
                ]
            )
        )

    env["BASH_ENV"] = bashrc.name
    env["PS1"] = "(" + env_name + " " + env_version + ")$ "
    if isdir(LHCB_ETC):
        env["VOMS_USERCONF"] = env.get("VOMS_USERCONF", join(LHCB_ETC, "vomses"))
        env["X509_CERT_DIR"] = env.get("X509_CERT_DIR", join(LHCB_ETC, "certificates"))
        env["X509_VOMS_DIR"] = env.get("X509_VOMS_DIR", join(LHCB_ETC, "vomsdir"))
        env["X509_VOMSES"] = env.get("X509_VOMSES", join(LHCB_ETC, "vomses"))

    if basename(command[0]) == "bash":
        exec_command = "set -x; exec bash --norc --noprofile"
        for c in command[1:]:
            exec_command += " " + pipes.quote(c)
    elif basename(command[0]) in ["sh", "ksh", "csh", "tcsh", "zsh", "fish"]:
        raise NotImplementedError(
            "Unable to launch %s as only bash is supported for now"
            % basename(command[0]),
        )
    else:
        exec_command = " ".join(pipes.quote(x) for x in command)

    logging.debug("Running command %s", exec_command)
    print(os.stat(bashrc.name))
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvpe("bash", ["bash", "--norc", "--noprofile", "-c", exec_command], env)


def lb_conda():
    """Invoke a commands in the correct environment"""
    parser = argparse.ArgumentParser(
        usage="lb-conda [-h] [--list] env_name[/version] [command] ...",
        description="Run a command in the LHCbDIRAC environment",
    )
    parser.add_argument("--list", action="store_true", help="List available versions")
    # argparse doesn't support optional positional arguments so use metavar to
    # set the help text
    positional_help_text = (
        "env_name  required, the name of the environment run\n  "
        "version   optional, the version of LHCbDIRAC to use (default: prod)\n  "
        "command   optional, the command to run (default: bash)\n  "
        "...       optional, any additional arguments"
    )
    parser.add_argument(
        "command",
        metavar=positional_help_text,
        default=["bash"],
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    # Handle --list
    if args.list or (len(args.command) >= 2 and args.command[1] == "--list"):
        if args.command:
            try:
                print(*sorted(DISPLAY_VERSIONS[args.command[0]]), sep="\n")
                sys.exit(0)
            except KeyError:
                sys.exit(2)
        else:
            print(*DISPLAY_VERSIONS, sep="\n")
            sys.exit(0)

    if len(args.command) == 0:
        raise NotImplementedError()

    env_name = args.command[0]
    command = args.command[1:] or ["bash"]

    if env_name in CONDA_ENVIRONMENTS:
        env_version = max(CONDA_ENVIRONMENTS[env_name])
    else:
        split_dirpath = env_name.split(os.sep)
        env_name = "/".join(split_dirpath[:-1])
        env_version = split_dirpath[-1]

        if env_name not in CONDA_ENVIRONMENTS:
            raise NotImplementedError()

        env_version = split_dirpath[-1]
        if env_version not in CONDA_ENVIRONMENTS[env_name]:
            raise NotImplementedError()

    # Try to replace the current process with the desired command
    try:
        call_in_conda(command, env_name, env_version)
    except Exception as e:
        logging.exception()
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(1)
