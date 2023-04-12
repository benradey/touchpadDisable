# touchpadDisable
A Python script that monitors for keystrokes and automatically dis-/re-enables the touchpad as appropriate

First, make sure the `touchpadDisable.py` file is owned by root and is read-only to other users. This is because the script reads directly from `/dev/input` which could otherwise enable keylogging and event spoofing.

Second, add the following near the bottom of your `sudoers` file:
`ben ALL=(ben:input) NOPASSWD: /home/ben/bin/touchpadDisable.py`

Third, configure your window manager to executet he following command on startup:
`sudo -g input /home/ben/bin/touchpadDisable.py`

Edit all values as appropriate. Enjoy!

