import minimal

class NAT_Minimal(minimal.Minimal):
    ''' Inter-LAN communication Minimal
    '''

    def __init__(self):
        super().__init__()

try:
    import argcomplete  # <tab> completion for argparse.
except ImportError:
    minimal.logging.warning("Unable to import argcomplete (optional)")

if __name__ == "__main__":
    minimal.parser.description = __doc__
    minimal.args = minimal.parser.parse_known_args()[0]
    try:
        argcomplete.autocomplete(minimal.parser)
    except Exception:
        minimal.logging.warning("argcomplete not working :-/")
    args = minimal.parser.parse_known_args()[0]

    if args.list_devices:
        print("Available devices:")
        print(minimal.sd.query_devices())
        quit()

    # if args.show_stats or args.show_samples or args.show_spectrum:
    #     if args.show_spectrum:
    #         import pygame  # If fails opening iris and swrast, run "export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6" (good idea to put it into .bashrc)
    #         import pygame_widgets
    #         import spectrum # If fails (DOLPHINS.WAV not found), update setuptools with "pip install setuptools"

    #     intercom = Minimal__verbose(args)
    # else:
    intercom = NAT_Minimal()

    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
        intercom.print_final_averages()