import argparse
import keyboard, mouse
import random
from time import sleep
from pranked.version import __version__


try:
    import winsound
except:
    pass


def _nop():
    pass

def _should_i(probability):
    return random.randint(0, 100) < probability

def _beep(frequency, duration):
    winsound.Beep(frequency, duration)

def _version(args):
    '''
    Runs when using version command
    '''
    print(__version__)


def _toggleable(toggle_key, kill_switch, turn_on, turn_off):
    def on():
        nonlocal current
        turn_on()
        current = off

    def off():
        nonlocal current
        turn_off()
        current = on

    kill_switch = kill_switch
    current = off
    turn_on()

    keyboard.add_hotkey(toggle_key, lambda: current())
    keyboard.wait(kill_switch)


def _repeat_key(args):
    toggle_key = args.toggle_key
    kill_switch  = args.kill_switch
    probability = args.probability
    key = args.key

    def repeat():
        if _should_i(probability):
            keyboard.write(key)

    def turn_on():
        nonlocal current
        current = repeat

    def turn_off():
        nonlocal current
        current = _nop

    current = _nop # Will be turned on immediately by _toggleable
    keyboard.add_hotkey(key, lambda: current())
    _toggleable(toggle_key, kill_switch, turn_on, turn_off)


def _beep_on_key(args):
    probability = args.probability
    kill_switch = args.kill_switch

    def on_press(x):
        if _should_i(probability):
            _beep(args.frequency, args.duration)

    keyboard.on_press(on_press)
    keyboard.wait(kill_switch)


def _block(args):
    blocked_key = args.key
    toggle_key = args.toggle_key
    kill_switch  = args.kill_switch
    hook = None

    def turn_on():
        nonlocal hook
        hook = keyboard.block_key(blocked_key)

    def turn_off():
        nonlocal hook
        keyboard.unblock_key(hook)
        hook = None

    _toggleable(toggle_key, kill_switch, turn_on, turn_off)


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
    parser = argparse.ArgumentParser(prog='pranked')
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument("-k", "--kill-switch", help="kill switch combination (default=c-m-k)", dest="kill_switch", default="ctrl+alt+k")
    parser.add_argument('-t', '--toggle', help='toggle (default=c-m-x)', default="ctrl+alt+x", dest="toggle_key")
    parser.add_argument('-w', '--wait', help='wait N minutes before active', type=int, default=0, dest="wait")
    subparsers = parser.add_subparsers(help='sub-command help')

    # version command parser
    subparser = subparsers.add_parser('version', help='returns version')
    subparser.set_defaults(func=_version)

   # upgrade parser
    subparser = subparsers.add_parser('upgrade', help='prints command to upgrade package')
    subparser.set_defaults(func=_upgrade)

    # kbtest
    subparser = subparsers.add_parser('kbtest', help='prints keyboard events')
    subparser.set_defaults(func=_kbtest)

    # repeat-key parser
    subparser = subparsers.add_parser('repeat', help='makes a key repeat itself')
    subparser.add_argument('key', help="key to be repeated")
    subparser.add_argument('-p', '--probability', help='probability in % (default=10)', type=int, default=10, dest='probability')
    subparser.set_defaults(func=_repeat_key)

    # beep parser
    subparser = subparsers.add_parser('beep', help='emits a beep on key presses')
    subparser.add_argument('-p', help='beep probability in % (default=10)', type=int, default=10, dest='probability')
    subparser.add_argument('-f', help='beep frequency', type=int, default=1000, dest='frequency')
    subparser.add_argument('-d', help='duration', type=int, default=50, dest='duration')
    subparser.set_defaults(func=_beep_on_key)

    # block parser
    subparser = subparsers.add_parser('block', help='block keyboard input')
    subparser.add_argument('key', help='key to be blocked')
    subparser.add_argument('-t', '--toggle', help='toggle', default="ctrl+alt+t", dest="toggle")
    subparser.set_defaults(func=_block)

    # crazymouse
    subparser = subparsers.add_parser('crazymouse', help='mouse cursor moves around randomly')
    subparser.add_argument('-d', '--delay', help='delay between moves (default=10)', default=10, type=int, dest="delay")
    subparser.add_argument('-s', '--speed', help="move speed (default=0)", default=0, type=int, dest="speed")
    subparser.set_defaults(func=_crazymouse)

    # magnify
    subparser = subparsers.add_parser('magnify', help='randomly magnify')
    subparser.add_argument('-d', '--delay', help='delay between magnifications (default=60)', default=60, type=int, dest="delay")
    subparser.set_defaults(func=_magnify)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'pranked' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    sleep(args.wait)
    args.func(args)
    keyboard.unhook_all()
