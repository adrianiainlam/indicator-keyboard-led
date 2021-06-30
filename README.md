# indicator-keyboard-led - simulate keyboard lock keys LED

This is a Unity application indicator designed for keyboards without lock
keys LED. It allows the user to check the state of the three locks (Caps lock,
Num lock and Scroll lock) without requiring any mouse or keyboard action. It
also allows the lock keys to be toggled with mouse clicks, which could be
useful for keyboards without Scroll lock keys or malfunctioning keyboards.

**Note**: This indicator is known to not work on Xfce / Xubuntu.
For more details, see [#6](https://github.com/adrianiainlam/indicator-keyboard-led/issues/6).

## Screenshots

![indicator default][sc1]  
Default appearance of the indicator with Num lock on and Caps and Scroll locks
off.

![indicator menu][sc2]  
Menu of the indicator, shown on click. The locks can be toggled by clicking
the respective item in the menu.

![indicator short][sc3]  
Alternative (short) appearance of the indicator.

## Installation from Ubuntu PPA

    sudo add-apt-repository ppa:adrianiainlam/indicator-keyboard-led
    sudo apt-get update
    sudo apt-get install indicator-keyboard-led

After installation the postinst script will prompt you for preferences
configuration. These config are explained here:

### Short label

The default appearance of the indicator has long labels:  
![⚫Num ⚫Caps ⚫Scroll][sc1]

On small displays it may be preferable to use short labels:  
![⚫N ⚫C ⚫S][sc3]

### Order

This option allows you to reorder the locks and also to hide
some locks if you don't need them.

Use a string consisting of zero or one occurrence of the
characters 'N', 'C' and 'S' to set this option.

For exampe, the default order is "Num Caps Scroll".  
![⚫Num ⚫Caps ⚫Scroll][sc1]

**CNS** changes this to "Caps Num Scroll".  
![⚫Caps ⚫Num ⚫Scroll][sc4]

**NC** hides Scroll lock from the default appearance.  
![⚫Num ⚫Caps][sc5]

**C**, combined with the previous *short* option,
would give a very compact Caps lock indicator.  
![⚫C][sc6]

[sc1]: screenshots/sc1.png
[sc2]: screenshots/sc2.png
[sc3]: screenshots/sc3.png
[sc4]: screenshots/sc4.png
[sc5]: screenshots/sc5.png
[sc6]: screenshots/sc6.png

### xdotool

`xdotool` is used to emulate key strokes to set/unset locks on mouse clicks.
If you installed xdotool at a non-default location, please provide its full
path (e.g. /home/user/bin/xdotool) with this option.

If it is installed in your $PATH environment variable, or not installed at
all, leave this option blank.

### Changing your mind

If you want to change these settings afterwards, simply run

    sudo dpkg-reconfigure indicator-keyboard-led

and you will be prompted again.

## Usage

The indicator will be configured to autostart on log-in. To start using the
indicator after installation, log-out and log-in again, or manually start
the indicator (search for "indicator-keyboard-led" in the dash).

The indicator should be shown at the top right corner, with a filled circle
representing a lock turned on and an unfilled circle representing a lock
turned off.

Clicking on the indicator should result in a menu with the three locks.
Clicking on the menu item would cause the corresponding lock to toggle.

## Known bugs / Troubleshooting

### Indicator label does not show on Xfce / XUbuntu

See [#6](https://github.com/adrianiainlam/indicator-keyboard-led/issues/6).

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
does not support [`gdk_keymap_get_scroll_lock_state ()`][gtkdoc-scroll].
The earliest Ubuntu release that supports GTK+ 3.18 is 16.04 (Xenial).
If you use an older version, Scroll lock functionality will be disabled.
Please consider upgrading your system if you really want Scroll lock.

If your installed GTK+ is 3.18+ then please file a bug report.

[gtkdoc-scroll]: https://developer.gnome.org/gdk3/stable/gdk3-Keyboard-Handling.html#gdk-keymap-get-scroll-lock-state

### Drop-down menu only has "Quit", the clickable locks do not appear

Please verify that xdotool is installed in your PATH with the executable
bit set. If you provided a custom path to xdotool please verify that it
is correct and is an executable regular file.

## Localization

As motivated by Issue #1, this script has been localized to French (with
the assistance of Wikipedia and Google Translate). Corrections to the
translation, as well as translations to other languages, are welcome.
Feel free to create a pull request or open an issue.

![indicator default, French locale][sc7]  
Default appearance in a French locale.

[sc7]: screenshots/sc7.png

## License

The program "indicator-keyboard-led.py" is released under the MIT License.
Please refer to the file for the full text of the license.

The icon "indicator-keyboard-led.svg" is released to the public domain.

## Credits

I would like to thank [Tobias Schlitt](https://github.com/tobyS), who wrote
[indicator-chars](https://github.com/tobyS/indicator-chars) which I used
as a reference when writing this software.

The icon used in the indicator (indicator-keyboard-led.svg) is modified
from the file "emblem-readonly.svg" by
[Jakub Steiner](http://jimmac.musichall.cz)
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
