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
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gdk, Gtk, AppIndicator3

class IndicatorKeyboardLED:
    locks = { 'num': 'Num', 'caps': 'Caps', 'scr': 'Scroll' }
    
    def __init__(self, short=False):
        self.indicator = AppIndicator3.Indicator.new(
            'indicator-keyboard-led',
            path.join(path.dirname(path.realpath(__file__)), 'icon.svg'),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        if short:
            self.locks = { 'num': 'N', 'caps': 'C', 'scr': 'S' }

        keymap = Gdk.Keymap.get_default()
        keymap.connect('state-changed', self.update_indicator)
        self.update_indicator(keymap)

        menu = Gtk.Menu()
        items = {
            'num'  : Gtk.MenuItem.new_with_label('Num Lock'),
            'caps' : Gtk.MenuItem.new_with_label('Caps Lock'),
            'scr'  : Gtk.MenuItem.new_with_label('Scroll Lock')
        }
        menu.append(items['num'])
        menu.append(items['caps'])
        menu.append(items['scr'])

        items['num' ].connect('activate', self.send_keypress, 'Num_Lock')
        items['caps'].connect('activate', self.send_keypress, 'Caps_Lock')
        items['scr' ].connect('activate', self.send_keypress, 'Scroll_Lock')

        self.indicator.set_menu(menu)
        menu.show_all()

    def update_indicator(self, keymap):
        label = '⚫' if keymap.get_num_lock_state() else '⚪'
        label += self.locks['num'] + ' '
        label += '⚫' if keymap.get_caps_lock_state() else '⚪'
        label += self.locks['caps'] + ' '
        label += '⚫' if keymap.get_scroll_lock_state() else '⚪'
        label += self.locks['scr']
        self.indicator.set_label(label, '')

    def send_keypress(self, menuitem, keystroke):
        subprocess.call(['xdotool', 'key', keystroke])

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signum, frame: Gtk.main_quit())
    
    parser = argparse.ArgumentParser(
        description='indicator-keyboard-led - simulate keyboard lock keys LED')
    parser.add_argument('-s', '--short', dest='short', action='store_true',
        help='use short label, i.e. ⚫N ⚫C ⚫S instead of ⚫Num ⚫Caps ⚫Scroll',
        required=False)
    args = parser.parse_args()
    
    IndicatorKeyboardLED(short=args.short)
    Gtk.main()
