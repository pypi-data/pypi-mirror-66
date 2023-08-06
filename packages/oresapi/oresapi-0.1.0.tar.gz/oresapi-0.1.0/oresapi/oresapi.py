"""
This script provides access to a set of utilities for ORES

* score_revisions -- Scores a set of revisions using an ORES API

{usage}
Options:
    -h | --help  Shows this documentation
    <utility>    The name of the utility to run
"""
import sys
import traceback
from importlib import import_module

USAGE = """Usage:
    {progname} (-h | --help)
    {progname} <utility> [-h | --help]
""".format(progname=sys.argv[0])


def main():

    if len(sys.argv) < 2:
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif sys.argv[1] in ("-h", "--help"):
        sys.stderr.write(__doc__.format(usage=USAGE))
        sys.exit(1)
    elif sys.argv[1][:1] == "-":
        sys.stderr.write(USAGE)
        sys.exit(1)

    module_name = sys.argv[1]
    module_path = ".utilities." + module_name

    try:
        sys.path.insert(0, ".")
        module = import_module(module_path, package="oresapi")
    except ImportError:
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write("Could not find module {0}.\n".format(module_path))
        sys.exit(1)

    module.main(sys.argv[2:])
