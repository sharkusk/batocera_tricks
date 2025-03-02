In order to use pre-2015 IPac controllers the following process can be used.  This likely works with any keyboard device!

* Find the name of your keyboard using the `evtest` application.  In my case there were several potential options for my IPAC-Mini, but through trial and error the one that responded to button presses was "`Ultimarc Button/Joystick/Trackball Interface`".
* Add a new entry to the `/etc/udev/rules.d/99-keyboardtopads.rules` along the lines of the following:
  ```
  # "Pre-2015 Ultimarc Mini-PAC"      : Xtention 2 players
  SUBSYSTEM=="input", KERNEL=="event*", ACTION=="add", ATTRS{name}=="Ultimarc*Button/Joystick/Trackball*Interface*", ENV{ID_INPUT_KEYBOARD}=="1",  ENV{ID_INPUT_KEYBOARD}="0", ENV{ID_INPUT_KEY}="0", ENV{ID_INPUT_KEYBOARDTOPADS}="1", RUN+="/usr/bin/keyboardToPadsLauncher $env{DEVNAME} run"
  ```
* Save your changes by running the `batocera-save-overlay` command and rebooting.

At this point you can follow the process documented here: https://wiki.batocera.org/diy-arcade-controls#arcade_controllers_keyboadtopads
