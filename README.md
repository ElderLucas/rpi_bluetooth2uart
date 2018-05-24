# rpi_bluetooth2uart


Finally I can pair my Raspberry Pi 3 with my Android phone without any user intervention on the Pi.

To do this you need to :

1) Create a file called "/usr/local/bin/auto-agent" containing the following code.

2) Make file executable

>> sudo chmod +x /usr/local/bin/auto-agent

3) Create a file called "/usr/local/bin/bluezutils.py" containing the following code.

4) Create a file called "BtAutoPair.py" (you can save this anywhere convenient) containing the following code.

5) Create a file called "testAutoPair.py (save this in the same directory as BtAutoPair.py) containing the following code.

That's it!

To check if it's working just run testAutoPair.py. You should then be able to pair your Pi to your phone without entering anything on the Pi.
If you are using legacy pairing then the code to enter on the phone is "0000".

You will need to install python-pexpect if it's not already installed.

>> sudo apt install python-pexpect

You will need to install python-dbus if it's not already installed.

>> sudo apt install python-dbus

To make the Pi permanently discoverable edit "/etc/bluetooth/main.conf" and change the line :

[ #DiscoverableTimeout = 0 ] To: [ DiscoverableTimeout = 0 ]

---------------------------------------
Ref: https://www.raspberrypi.org/forums/viewtopic.php?t=170353
Ref: https://gist.github.com/egorf/66d88056a9d703928f93
