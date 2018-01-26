#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from string import ascii_lowercase, ascii_uppercase
from copy import copy
import logging
from pyVmomi import vim

logger = logging.getLogger(__name__)


# Constants derived from http://www.win.tue.nl/~aeb/linux/kbd/scancodes-14.html and https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
KEY_MOD_LCTRL = 0x01
KEY_MOD_LSHIFT = 0x02
KEY_MOD_LALT = 0x04
KEY_MOD_LMETA = 0x08
KEY_MOD_RCTRL = 0x10
KEY_MOD_RSHIFT = 0x20
KEY_MOD_RALT = 0x40
KEY_MOD_RMETA = 0x80

# Friendly names for modifiers. Only bother implementing the Left side.
MODIFIERS = {
    "shift": KEY_MOD_LSHIFT,
    "alt": KEY_MOD_LALT,
    "meta": KEY_MOD_LMETA,
    "ctrl": KEY_MOD_LCTRL,
}

def _generate(iterable, base_value, modifier=()):
    """From an sequence of characters, emit a sequence of scancodes starting from base_value and incrementing by 1."""
    for c in iterable:
        yield (c, (base_value, modifier))
        base_value += 1


CHARACTERS = dict()
CHARACTERS.update(dict(_generate(ascii_lowercase, 0x04)))
CHARACTERS.update(dict(_generate("1234567890", 0x1e)))

CHARACTERS.update(dict(_generate(' ', 0x2c)))

CHARACTERS.update(dict(_generate('-=[]\\', 0x2d)))
CHARACTERS.update(dict(_generate(";'`,./", 0x33)))

CHARACTERS.update(dict(_generate(ascii_uppercase, 0x04, (KEY_MOD_LSHIFT,))))
CHARACTERS.update(dict(_generate("!@#$%^&*()", 0x1e, (KEY_MOD_LSHIFT,))))

CHARACTERS.update(dict(_generate("_+{}|", 0x2d, (KEY_MOD_LSHIFT,))))
CHARACTERS.update(dict(_generate(':"~<>?', 0x33, (KEY_MOD_LSHIFT,))))


# Construct a hash of friendly key-names
KEYS = copy(CHARACTERS)

# Function keys
KEYS.update(dict(_generate(["F%d" for d in range(1,12)], 0x3a, ())))


KEYS.update({
    'enter': (0x28, ()),
    'esc': (0x29, ()), 'escape': (0x29, ()),

    'backspace': (0x2a, ()),
    'tab': (0x2b, ()),

    'sysrq': (0x46, ()), 'printscreen': (0x46, ()),
    'scrolllock': (0x47, ()),
    'pause': (0x48, ()),
    'insert': (0x49, ()),
    'home': (0x4a, ()),
    'pageup': (0x4b, ()),
    'delete': (0x4c, ()),
    'end': (0x4d, ()),
    'pagedown': (0x4e, ()),
    'right': (0x4f, ()),
    'left': (0x50, ()),
    'down': (0x51, ()),
    'up': (0x52, ())
})


def hid_scancode_to_key_event(scancode, modifiers):
    """Convert a single scancode + modifier list to a vSphere vim KeyEvent instance suitible for transmission."""

    # bitwise shift left 16, boolean or with 7
    event = vim.UsbScanCodeSpecKeyEvent()
    event.usbHidCode = (scancode << 16) | 7

    if modifiers:
        event.modifiers = vim.UsbScanCodeSpecModifierType()
        if KEY_MOD_LSHIFT in modifiers:
            event.modifiers.leftShift = True
        if KEY_MOD_LCTRL in modifiers:
            event.modifiers.leftControl = True
        if KEY_MOD_LMETA in modifiers:
            event.modifiers.leftGui = True
        if KEY_MOD_LALT in modifiers:
            event.modifiers.leftAlt = True
        if KEY_MOD_RSHIFT in modifiers:
            event.modifiers.rightShift = True
        if KEY_MOD_RCTRL in modifiers:
            event.modifiers.rightControl = True
        if KEY_MOD_RMETA in modifiers:
            event.modifiers.rightGui = True
        if KEY_MOD_RALT in modifiers:
            event.modifiers.rightAlt = True
    return event


def transmit_key_events(virtualmachine, q):
    """
    API call completes quickly, but key-presses may be queued (eg ~1s) before reaching the GuestOS.

    Calling PutUsbScanCodes() with too many scancodes can result in overrun/drops.
    Iterate over the list `q`, and transmit one at a time.
    """
    transmitted_quantity = 0
    for item in q:
        s = vim.UsbScanCodeSpec()
        s.keyEvents.append(item)
        transmitted_quantity += virtualmachine.PutUsbScanCodes(s)
    return transmitted_quantity


def _setup_logger(args):
    """Set up logging according to command-line verbosity"""
    import sys
    logger = logging.getLogger()
    logger.setLevel(int(30 - (args.loglevel * 10)))
    ch = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(u'%(asctime)s %(name)s %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Set logging level to {0}".format(logging.getLevelName(logger.getEffectiveLevel())))
    return logger


def _arguments():
    import argparse

    try:
        # Try to discover the window size, so argparse can draw appropriately-wrapped help.
        import shutil
        import os
        os.environ['COLUMNS'] = str(min([120, shutil.get_terminal_size().columns]))
    except:
        pass  # If that's not possible, carry on.

    top = argparse.ArgumentParser()

    top.add_argument("keys",
                     nargs='*',
                     help="Keys to transmit, like 'a' or 'up' or 'ctrl+alt+delete'. Can be listed multiple times, with each instance mapped to a single transmission.")

    top.add_argument("-c", "--characters", default="", metavar="C",
                     help="List of characters in a quoted string, like 'abcd'. Can be listed multiple times.")

    top.add_argument("--raw-scancode", default=[], action="append", type=int, metavar="I", help="An integer scancode. Can be listed multiple times.")

    top.add_argument("--modifier", default=[], action="append", choices=MODIFIERS.keys(), help="Modifier to be added to everything transmitted. Can be listed multiple times.")

    target = top.add_argument_group("Target Virtual Machine")
    target.add_argument("--moref", help="Virtual Machine moref number, like '13'")
    target.add_argument("--uuid", help="BIOS UUID, such as /sys/class/dmi/id/product_uuid")
    target.add_argument("--ip", help="IP address reported by the VMware Tools")

    loggroup = top.add_argument_group("Display")
    loggroup.add_argument("-v", "--verbose", action="count", default=0, dest="loglevel", help="Slightly more logging.")
    loggroup.add_argument("--whatif", action="store_true", help="Display the vim.vm.UsbScanCodeSpec.KeyEvent objects and exit.")

    certgroup = top.add_argument_group("Certificates")
    certgroup.add_argument("--insecure", action="store_false", default=True, dest="verify",
                           help="Let someone MITM your HTTTPS connection.")

    accountgroup = top.add_argument_group("vSphere")
    accountgroup.add_argument("--hostname",
                              default="localhost",
                              metavar='vCenter Server or ESXi host')
    accountgroup.add_argument("--port", default=443, metavar='vCenter Server Port')
    accountgroup.add_argument("--username",
                              default="root",
                              help="Login to vCenter Server with this username.")
    accountgroup.add_argument("--password",
                              default="VMware123!",
                              help="Login to vCenter Server with this password.")


    args = top.parse_args()
    return top, args


if __name__ == "__main__":
    from pyVim.connect import SmartConnect
    import ssl

    parser, args = _arguments()

    _setup_logger(args)

    # Create the list of requested scancodes
    global_requested_modifiers = [MODIFIERS[k] for k in MODIFIERS if k in args.modifier]

    transmit = []
    for c in args.characters:
        scancode, modifier = CHARACTERS[c]
        if global_requested_modifiers:
            modifier = global_requested_modifiers + list(modifier)
        transmit.append(hid_scancode_to_key_event(scancode, modifier))

    for scancode in args.raw_scancode:
        transmit.append(hid_scancode_to_key_event(scancode, global_requested_modifiers))

    for key in args.keys:
        if key[-2:] == "++":
            keybits = key[0:-2].split("+")  # Handle syntax like ctrl++
            keybits.append("+")
        elif "+" in key and len(key)>2:
            keybits = key.split("+")  # Handle syntax like ctrl+alt+b
        else:
            keybits = [key]  # Bare characters

        scancode, modifier = KEYS[keybits[-1]]

        scoped_modifiers = list(modifier)  # Copy the tuple to a list, so we can modify it.

        if global_requested_modifiers:
            scoped_modifiers += global_requested_modifiers

        for modifier_prefix in keybits[0:-1]:
            scoped_modifiers.append(MODIFIERS[modifier_prefix])

        transmit.append(hid_scancode_to_key_event(scancode, scoped_modifiers))

    if args.whatif:
        if not transmit:
            print("Nothing to transmit")
        for k in transmit:
            print(k)
        parser.exit(0)

    # Setup network connection to a remote server
    if not args.verify:
        import ssl
        context = ssl._create_unverified_context()
    else:
        context = None

    si = SmartConnect(
        host=args.hostname,
        user=args.username,
        pwd=args.password,
        port=int(args.port),
        sslContext=context
    )

    logger.info("Authenticated to {0} as {1}={2}".format(
        si.content.about.fullName,
        si.content.sessionManager.currentSession.key,
        si.content.sessionManager.currentSession.userName
    ))

    vm = None
    if args.moref:
        vm = vim.VirtualMachine(args.moref)
        vm._stub = si._stub
    elif args.uuid:
        search_index = si.content.searchIndex
        vm = search_index.FindByUuid(None, args.uuid, True, True)
    elif args.ip:
        search_index = si.content.searchIndex
        vm = search_index.FindByIp(None, args.ip, True)
    else:
        parser.error("Require one of (moref, uuid, ip)")

    n = transmit_key_events(virtualmachine=vm, q=transmit)
    logger.debug("Sent %d key events." % n)
