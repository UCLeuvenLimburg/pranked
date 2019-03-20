import argparse 
import keyboard
import random
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

def _beep(args):
    probability = args.probability
    kill_switch = args.kill_switch

    def beep():
        print('\a')

    def on_press(x):
        if random.randint(0, 100) < probability:
            beep()

    keyboard.on_press(on_press)
    keyboard.wait(kill_switch)

def _upgrade(args):
    print("pip install --upgrade git+https://github.com/UCLeuvenLimburg/pranked.git")

def _create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    # Top level parser
    parser = argparse.ArgumentParser(prog='scripting')
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument("--kill-switch", help="kill switch combination (default=c-m-k)", dest="kill_switch", default="ctrl+alt+k")
    subparsers = parser.add_subparsers(help='sub-command help')

    # version command parser
    subparser = subparsers.add_parser('version', help='returns version')
    subparser.set_defaults(func=_version)

    # repeat-key parser
    subparser = subparsers.add_parser('repeat-key', help='makes a key repeat itself')
    subparser.add_argument('key', help="key to be repeated")
    subparser.set_defaults(func=_repeat_key)

    # upgrade parser
    subparser = subparsers.add_parser('upgrade', help='prints command to upgrade package')
    subparser.set_defaults(func=_upgrade)

    # beep parser
    subparser = subparsers.add_parser('beep', help='emits a beep on key presses')
    subparser.add_argument('-p', help='beep probability in % (default=10)', type=int, default=10, dest='probability')
    subparser.set_defaults(func=_beep)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    args.func(args)
    keyboard.unhook_all()