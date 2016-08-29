#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# indicator-keyboard-led - simulate keyboard lock keys LED
# Copyright (c) 2016 Adrian I Lam <adrianiainlam@gmail.com>
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
from os import path
import argparse
import sys
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gdk, Gtk, AppIndicator3

class IndicatorKeyboardLED:
    locks = { 'N': 'Num', 'C': 'Caps', 'S': 'Scroll' }
    
    def __init__(self, short=False, order='NCS'):
        self.indicator = AppIndicator3.Indicator.new(
            'indicator-keyboard-led',
            path.join(path.dirname(path.realpath(__file__)), 'icon.svg'),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        if short:
            self.locks = { 'N': 'N', 'C': 'C', 'S': 'S' }

        keymap = Gdk.Keymap.get_default()
        keymap.connect('state-changed', self.update_indicator, order)
        self.update_indicator(keymap, order)

        menu = Gtk.Menu()
        items = {
            'N': Gtk.MenuItem.new_with_label('Num Lock'),
            'C': Gtk.MenuItem.new_with_label('Caps Lock'),
            'S': Gtk.MenuItem.new_with_label('Scroll Lock')
        }
        items['N'].connect('activate', self.send_keypress, 'Num_Lock')
        items['C'].connect('activate', self.send_keypress, 'Caps_Lock')
        items['S'].connect('activate', self.send_keypress, 'Scroll_Lock')

        for i in order:
            menu.append(items[i])

        quit_item = Gtk.MenuItem.new_with_label('Quit')
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(quit_item)
        quit_item.connect('activate', Gtk.main_quit)

        self.indicator.set_menu(menu)
        menu.show_all()

    def update_indicator(self, keymap, order):
        labels = []
        for i in order:
            if i == 'N':
                state = keymap.get_num_lock_state()
            elif i == 'C':
                state = keymap.get_caps_lock_state()
            elif i == 'S':
                state = keymap.get_scroll_lock_state()
            else:
                raise ValueError('Invalid value in ORDER')
            labels += [('⚫' if state else '⚪') + self.locks[i]]
        self.indicator.set_label(' '.join(labels), '')

    def send_keypress(self, menuitem, keystroke):
        subprocess.call(['xdotool', 'key', keystroke])

def validate_order(args):
    args.order = args.order.upper()
    for i in args.order:
        if i not in ['N', 'C', 'S']:
            sys.exit('Illegal character in ORDER. (Choices: [N, C, S])')
    if len(args.order) != len(set(args.order)):
        sys.exit('Repeated character in ORDER. '
                 'Please specify each lock at most once.')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signum, frame: Gtk.main_quit())

    parser = argparse.ArgumentParser(
        description='indicator-keyboard-led - simulate keyboard lock keys LED',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--short', action='store_true',
        help='use short label, i.e. ⚫N ⚫C ⚫S instead of ⚫Num ⚫Caps ⚫Scroll',
        required=False)
    parser.add_argument('-o', '--order', required=False, default='NCS',
        help='specify the order of the locks displayed, e.g. CSN for '
             '⚫Caps ⚫Scroll ⚫Num, or NC for ⚫Num ⚫Caps without Scroll lock')
    args = parser.parse_args()
    validate_order(args)

    IndicatorKeyboardLED(short=args.short, order=args.order)
    Gtk.main()
