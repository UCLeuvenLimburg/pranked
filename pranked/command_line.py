import argparse 
import keyboard, mouse
import random
from time import sleep
from pranked.version import __version__


try:
    import winsound
except:
    pass


def _beep(frequency, duration):
    winsound.Beep(frequency, duration)

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

def _beep_on_key(args):
    probability = args.probability
    kill_switch = args.kill_switch

    def on_press(x):
        if random.randint(0, 100) < probability:
            _beep(args.frequency, args.duration)

    keyboard.on_press(on_press)
    keyboard.wait(kill_switch)

def _block(args):
    kill_switch = args.kill_switch
    toggle_key = args.toggle
    blocked_key = args.key
    hook = keyboard.block_key(blocked_key)

    def on_toggle():
        nonlocal hook
        if hook:
            keyboard.unblock_key(hook)
            hook = None
        else:
            keyboard.block_key(blocked_key)        

    keyboard.add_hotkey(toggle_key, on_toggle)
    keyboard.wait(kill_switch)


def _crazymouse(args):
    kill_switch = args.kill_switch
    delay = args.delay
    speed = args.speed
    active = True

    def on_kill():
        nonlocal active
        active = False

    keyboard.add_hotkey(kill_switch, on_kill)

    while active:
        dx = random.randint(-500, 500)
        dy = random.randint(-500, 500)
        mouse.move(dx, dy, absolute=False, duration=speed)
        sleep(delay)


def _kbtest(args):
    kill_switch = args.kill_switch

    def on_press(key):
        print(key, flush=True)

    keyboard.on_press(on_press)
    keyboard.wait(kill_switch)


def _magnify(args):
    kill_switch = args.kill_switch
    delay = args.delay
    active = True

    def on_kill():
        nonlocal active
        active = False

    def magnify():
        keyboard.send('windows+plus')
        sleep(1)
        keyboard.send('windows+plus')

    keyboard.add_hotkey(kill_switch, on_kill)

    while active:
        magnify()
        sleep(delay)


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
    subparser.add_argument('-f', help='beep frequency', type=int, default=1000, dest='frequency')
    subparser.add_argument('-d', help='duration', type=int, default=50, dest='duration')
    subparser.set_defaults(func=_beep_on_key)

    # block parser
    subparser = subparsers.add_parser('block', help='block keyboard input')
    subparser.add_argument('key', help='key to be blocked')
    subparser.add_argument('-t', help='toggle', default="ctrl+alt+t", dest="toggle")
    subparser.set_defaults(func=_block)

    # crazymouse
    subparser = subparsers.add_parser('crazymouse', help='mouse cursor moves around randomly')
    subparser.add_argument('-d', '--delay', help='delay between moves (default=10)', default=10, type=int, dest="delay")
    subparser.add_argument('-s', '--speed', help="move speed (default=0)", default=0, type=int, dest="speed")
    subparser.set_defaults(func=_crazymouse)

    # kbtest
    subparser = subparsers.add_parser('kbtest', help='prints keyboard events')
    subparser.set_defaults(func=_kbtest)

    # magnify
    subparser = subparsers.add_parser('magnify', help='randomly magnify')
    subparser.add_argument('-d', '--delay', help='delay between magnifications (default=60)', default=60, type=int, dest="delay")
    subparser.set_defaults(func=_magnify)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    args.func(args)
    keyboard.unhook_all()
