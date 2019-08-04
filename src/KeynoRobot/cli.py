# Copyright 2013 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import argparse

#from KeynoRobot._installed import Installed


# def _registered_commands(group='KeynoRobot.registered_commands'):
    # registered_commands = pkg_resources.iter_entry_points(group=group)
    # return {c.name: c for c in registered_commands}


# def list_dependencies_and_versions():
    # return [
        # ('pkginfo', Installed(pkginfo).version),
        # ('requests', requests.__version__),
        # ('setuptools', setuptools.__version__),
        # ('requests-toolbelt', requests_toolbelt.__version__),
        # ('tqdm', tqdm.__version__),
    # ]


# def dep_versions():
    # return ', '.join(
        # '{}: {}'.format(*dependency)
        # for dependency in list_dependencies_and_versions()
    # )

print(__name__)



""""
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest]
    name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action - The basic type of action to be taken when this argument is encountered at the command line.
    nargs - The number of command-line arguments that should be consumed.
    const - A constant value required by some action and nargs selections.
    default - The value produced if the argument is absent from the command line.
    type - The type to which the command-line argument should be converted.
    choices - A container of the allowable values for the argument.
    required - Whether or not the command-line option may be omitted (optionals only).
    help - A brief description of what the argument does.
    metavar - A name for the argument in usage messages.
    dest -  The name of  the attribute to be added to the object returned by parse_args().  
"""