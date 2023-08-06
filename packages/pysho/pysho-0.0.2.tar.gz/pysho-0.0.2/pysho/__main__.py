import os
import sys
import subprocess
from .core import *
from .console import run_console

# scripts inherit what we've imported above here
DEFAULT_VARIABLES = globals()


def run_file(script_file, debug=False, variables=DEFAULT_VARIABLES):
    variables["SCRIPT"] = os.path.abspath(script_file)
    variables["SCRIPT_DIR"] = os.path.dirname(variables["SCRIPT"])
    with open(script_file, "r") as scriptfile:
        text = scriptfile.read()
    return run_string(text, debug=debug, variables=variables)


def run_string(script_text, debug=False, variables=DEFAULT_VARIABLES):
    try:
        variables["INITIAL_DIR"] = os.getcwd()
        exec(script_text, variables, locals())
    except Exception as err:
        if debug:
            raise
        else:
            if "SCRIPT" in variables:
                print("error processing '{}':".format(variables["SCRIPT"]))
            print(sys.stderr, str(err))
            sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("SCRIPT", type=str, nargs="?",
                        help="The script to execute.", default=None)
    parser.add_argument("-c", "--command", type=str,
                        help="Run the given string as a script")
    parser.add_argument("-s", "--stdin", default=False, action="store_true",
                        help="Read the script from stdin")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Print stack traces")

    if WINDOWS:
        # options for registering file extensions
        parser.add_argument("--register", default=False, action="store_true",
                            help="Register .pysho file extensions (requires administrator privs)")

    opts = parser.parse_args()

    if hasattr(opts, "register") and opts.register:
        for ext in ["pysh", "pysho"]:
            subprocess.check_call(["cmd", "/C", "assoc", ".{}=pyshofile".format(ext)])
        subprocess.check_call(["cmd", "/C", "ftype", "pyshofile=" + sys.executable, "-m", "pysho", "%1"])
    else:
        if opts.command:
            run_string(opts.command)
        elif opts.stdin:
            script = str(sys.stdin.read())
            run_string(script)
        elif opts.SCRIPT:
            run_file(opts.SCRIPT)
        else:
            run_console(globals(), locals())


if __name__ == "__main__":
    main()

