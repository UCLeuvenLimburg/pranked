import argparse 
import keyboard
from pranked.version import __version__


def _version(args):
    '''
    Runs when using version command
    '''
    print(__version__)


def _repeat_key(args):
    key = args.key
    kill_switch = args.kill_switch

    def on_key_pressed():
        keyboard.write(key)
    
    keyboard.add_hotkey(key, on_key_pressed)
    keyboard.wait(kill_switch)


def _create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    # Top level parser
    parser = argparse.ArgumentParser(prog='scripting')
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument("--kill-switch", help="kill switch combination (default=c-m-k)", dest="kill_switch", default="ctrl+alt+k")
    subparsers = parser.add_subparsers(help='sub-command help')

    # Version command parser
    test_parser = subparsers.add_parser('version', help='returns version')
    test_parser.set_defaults(func=_version)

    # Test command parser
    test_parser = subparsers.add_parser('repeat-key', help='makes a key repeat itself')
    test_parser.add_argument('key', help="key to be repeated")
    test_parser.set_defaults(func=_repeat_key)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    args.func(args)
