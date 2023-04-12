# touchpadDisable
A Python script that monitors for keystrokes and automatically dis-/re-enables the touchpad as appropriate.
Also controls the Legion RGB keyboard!

[Credit for the l5p_kbl library](https://github.com/imShara/l5p-kbl)
[Credit for the legion_laptop kernel module](https://github.com/johnfanv2/LenovoLegionLinux)

First, make sure the `touchpadDisable.py` and `l5p_kbl.py` files are owned by root and read-only to other users. This is because the script reads directly from `/dev/input` which could otherwise enable keylogging and event spoofing.

Second, add the following near the bottom of your `sudoers` file:
`ben ALL=(ben:input) NOPASSWD: /home/ben/bin/touchpadDisable.py`

Third, configure your window manager to execute the following command on startup:
`sudo -g input /home/ben/bin/touchpadDisable.py`

Also requires installing the legion_laptop kernel module linked above.

Edit all values as appropriate. Enjoy!

