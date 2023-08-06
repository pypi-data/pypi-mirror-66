import code


class ReadlineConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>"):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            import readline
            readline.parse_and_bind("tab: complete")
        except ImportError:
            pass


def run_console(globals, locals):
    try:
        from ptpython.repl import embed
        embed(globals, locals, vi_mode=False, history_filename=None)
    except Exception:
        import sys
        con = ReadlineConsole(locals=globals)
        if sys.version_info[0] > 2:
            con.interact("pysho:", "exiting pysho..")
        else:
            con.interact("pysho")
