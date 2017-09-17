# indicator-keyboard-led - simulate keyboard lock keys LED

This is a Unity application indicator designed for keyboards without lock
keys LED. It allows the user to check the state of the three locks (Caps lock,
Num lock and Scroll lock) without requiring any mouse or keyboard action. It
also allows the lock keys to be toggled with mouse clicks, which could be
useful for keyboards without Scroll lock keys or malfunctioning keyboards.

## Screenshots

![indicator default][sc1]  
Default appearance of the indicator with Num lock on and Caps and Scroll locks
off.

![indicator menu][sc2]  
Menu of the indicator, shown on click. The locks can be toggled by clicking
the respective item in the menu.

![indicator short][sc3]  
Alternative (short) appearance of the indicator.

## Dependencies
 - Python 3 (*)
 - GTK+ 3 (*)
 - AppIndicator 3 (*)
 - Python 3 GObject introspection (python3-gi)
 - xdotool

Those marked with (*) are probably installed by default in recent Ubuntu
distributions. To install the rest, run:

    sudo apt-get install python3-gi xdotool

**Note**: [`gdk_keymap_get_scroll_lock_state ()`][gtkdoc-scroll] is only
available since GTK+ 3.18. The earliest Ubuntu release that supports
GTK+ 3.18 is 16.04 (Xenial). This means that if you use an older version,
scroll lock functionality will be disabled.

[gtkdoc-scroll]: https://developer.gnome.org/gdk3/stable/gdk3-Keyboard-Handling.html#gdk-keymap-get-scroll-lock-state

## Usage

 1. Install the dependencies listed above.
 2. Clone this repository.
 3. Add the script as a startup application. (Use option `--short` for short
    appearance; use option `--order` to customize the order of the locks
    displayed. See [Examples](#examples))
 4. Run the script manually for the first time. (Alternatively, log out
    and log in again.)
 5. The indicator should be shown at the top right corner, with a filled circle
    representing a lock turned on and an unfilled circle representing a lock
    turned off.
 6. Clicking on the indicator should result in a menu with the three locks.
    Clicking on the menu item would cause the corresponding lock to toggle.

## Examples

![indicator default][sc1]  
Default appearance. `python3 indicator-keyboard-led.py`

![indicator short][sc3]  
Short appearance. `python3 indicator-keyboard-led.py --short`

![indicator CNS][sc4]  
Order changed to Caps Num Scroll.
`python3 indicator-keyboard-led.py --order CNS`

![indicator NC][sc5]  
Hide Scroll lock, also the default appearance if Scroll lock is not supported. `python3 indicator-keyboard-led.py --order NC`

![indicator C short][sc6]  
Show Caps lock only, short appearance.
`python3 indicator-keyboard-led.py --short --order C`

![indicator default, French locale][sc7]  
Default appearance in a French locale.
`LANGUAGE=fr_FR python3 indicator-keyboard-led.py`

[sc1]: screenshots/sc1.png
[sc2]: screenshots/sc2.png
[sc3]: screenshots/sc3.png
[sc4]: screenshots/sc4.png
[sc5]: screenshots/sc5.png
[sc6]: screenshots/sc6.png
[sc7]: screenshots/sc7.png

## Known bugs / Troubleshooting

### Pressing Scroll Lock does nothing

It seems to be a common problem that Scroll Lock is not usable in Ubuntu.
To solve this, do the following (assuming US keyboard):

 >     # backup your symbols file
 >     sudo cp /usr/share/X11/xkb/symbols/us{,.distribution} 
 >
 > Add the following line in the `xkb_symbols "basic" {` section. Do not worry
 > if that second line is not there, it is only there for some languages and
 > was not there for us on my system.
 >
 >     ...
 >         modifier_map Mod3   { Scroll_Lock }; <==<< Add this line
 > 
 >         include "level3(ralt_switch)" <==<< before this line
 >     };
 >
 >
 > You may have to do the same in your other layouts if you switch between
 > languages.
 >
 > Also, there is a cache where xkb layouts live. You should clear it before
 > restarting your X server to check the new keyboard symbol file(s).
 >
 >     sudo dpkg-reconfigure xkb-data

*By Pykler and Giovanni Toraldo on AskUbuntu.* [Source][quotesrc]. Slightly
modified. [Original source][origsrc] by dm+ on PCLinuxOS-Forums.

[origsrc]: http://www.pclinuxos.com/forum/index.php/topic,125690.msg1052201.html?PHPSESSID=2qsv83lve6dgd0ivq14bfcjc30#msg1052201
[quotesrc]: http://askubuntu.com/a/597757/274080

### Scroll lock does not appear on indicator

Your installed GTK+ version is probably older than 3.18, which
does not support `get_scroll_lock_state`. Please consider upgrading
your system if you really want Scroll lock functionality.

If your installed GTK+ is 3.18+ then please file a bug report.

### Drop-down menu only has "Quit", the clickable locks do not appear

Please verify that xdotool is installed in your PATH with the executable
bit set. If you provided a custom path to xdotool please verify that it
is correct and is an executable regular file.

## Localization

As motivated by Issue #1, this script has been localized to French (with
the assistance of Wikipedia and Google Translate). Corrections to the
translation, as well as translations to other languages, are welcome.
Feel free to create a pull request or open an issue.

## License

The program "indicator-keyboard-led.py" is released under the MIT License.
Please refer to the file for the full text of the license.

The icon "icon.svg" is released to the public domain.

## Credits

I would like to thank [Tobias Schlitt](https://github.com/tobyS), who wrote
[indicator-chars](https://github.com/tobyS/indicator-chars) which I used
as a reference when writing this software.

The icon used in the indicator (icon.svg) is modified from the file
"emblem-readonly.svg" by [Jakub Steiner](http://jimmac.musichall.cz)
who released it to the public domain for the
[Tango Icon Library](http://tango.freedesktop.org/Tango_Icon_Library).

---

## Motivation

I was a user of [indicator-keylock][ind-kl], but only one key lock can be shown
on the panel. I didn't like the Notify OSD events either.

I then came across [lks-indicator][lks] and [indicator-xbdmod][xbdmod], but
I didn't like the fact that they refresh the indicator on a regular time
interval (every *x* milliseconds) rather than on state changes (only when
the locks are toggled).

I also thought it would be fun to be able to toggle the locks on-screen.

[ind-kl]: https://launchpad.net/~tsbarnes/+archive/ubuntu/indicator-keylock
[lks]: https://github.com/SergKolo/lks-indicator
[xbdmod]: https://github.com/sneetsher/indicator-xkbmod
