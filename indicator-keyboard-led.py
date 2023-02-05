#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# indicator-keyboard-led - simulate keyboard lock keys LED
# Copyright (c) 2017-2023 Adrian I Lam <spam@adrianiainlam.tk> s/spam/me/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# I would like to thank Tobias Schlitt <toby@php.net>, who wrote
# indicator-chars <https://github.com/tobyS/indicator-chars> which I used
# as a reference when writing this software.

import signal
import subprocess
import os
import argparse
import shutil
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gdk, Gtk, AppIndicator3

APP_NAME = 'indicator-keyboard-led'
APP_VERSION = '1.2'

ICON_FOLDER = '/usr/share/icons/hicolor/scalable/apps/'
import gettext
t = gettext.translation(APP_NAME, '/usr/share/locale')
_ = t.gettext

class IndicatorKeyboardLED:
    def __init__(self, order='NCS', xdotool=None):
        self.validate_order(order)

        self.indicators = {}

        count = 0
        for i in order:
            self.indicators[i] = AppIndicator3.Indicator.new(
                '-'.join([APP_NAME, str(count), i]),
                os.path.join(ICON_FOLDER, '-'.join([APP_NAME, i, 'off.svg'])),
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.indicators[i].set_status(AppIndicator3.IndicatorStatus.ACTIVE)

            count += 1

        keymap = Gdk.Keymap.get_default()
        keymap.connect('state-changed', self.update_indicator, order)
        self.update_indicator(keymap, order)
        self.create_menu(xdotool, order)

    def create_menu(self, xdotool, order):
        xdotool = xdotool or shutil.which('xdotool')
        def send_keypress(menuitem, keystroke):
            subprocess.call([xdotool, 'key', keystroke])
        def new_menu_item(itemtype):
            if itemtype == 'N':
                item = Gtk.MenuItem.new_with_label(_('Num Lock'))
                item.connect('activate', send_keypress, 'Num_Lock')
            elif itemtype == 'C':
                item = Gtk.MenuItem.new_with_label(_('Caps Lock'))
                item.connect('activate', send_keypress, 'Caps_Lock')
            elif itemtype == 'S':
                item = Gtk.MenuItem.new_with_label(_('Scroll Lock'))
                item.connect('activate', send_keypress, 'Scroll_Lock')
            else:
                raise ValueError('Invalid itemtype')
            return item

        for i in order:
            menu = Gtk.Menu()

            if xdotool and os.access(xdotool, os.X_OK) and os.path.isfile(xdotool):
                menu.append(new_menu_item(i))

            quit_item = Gtk.MenuItem.new_with_label(_('Quit'))
            menu.append(quit_item)
            quit_item.connect('activate', Gtk.main_quit)

            self.indicators[i].set_menu(menu)
            menu.show_all()

    def update_indicator(self, keymap, order):
        for i in order:
            if i == 'N':
                state = keymap.get_num_lock_state()
            elif i == 'C':
                state = keymap.get_caps_lock_state()
            elif i == 'S':
                state = keymap.get_scroll_lock_state()
            else:
                raise ValueError('Invalid value in ORDER')

            icon = os.path.join(ICON_FOLDER, '-'.join([APP_NAME, i, 'on.svg' if state else 'off.svg']))
            self.indicators[i].set_icon(icon)


    def validate_order(self, order):
        order = order.upper()
        for i in order:
            if i not in ['N', 'C', 'S']:
                raise ValueError('Illegal character in ORDER. '
                                 '(Choices: [N, C, S])')
        if len(order) != len(set(order)):
            raise ValueError('Repeated character in ORDER. '
                             'Please specify each lock at most once.')
        if 'S' in order and Gtk.check_version(3, 18, 0) is not None:
            # Silently drop Scroll lock if GTK <= 3.18
            order.remove('S')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signum, frame: Gtk.main_quit())

    parser = argparse.ArgumentParser(
        description='indicator-keyboard-led - simulate keyboard lock keys LED',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--order', required=False, default='NCS',
        help='specify the order of the locks displayed, e.g. CSN for '
             'Caps Scroll Num, or NC for Num Caps without Scroll lock')
    parser.add_argument('-x', '--xdotool', required=False,
        help='provide full path to xdotool executable, '
             'e.g. "/usr/bin/xdotool"; '
             'if not specified, search in PATH')
    args = parser.parse_args()

    IndicatorKeyboardLED(order=args.order,
                         xdotool=args.xdotool)
    Gtk.main()
