# Digital Frame

This repo holds code and instructions to run a simple python script for homemade digital photo frames. It is meant to run on Raspberry Pi OS Lite (but the instructions can be tweaked fairly easily to work on any OS). 

The script itself (`main.py`) fetches any new photos from an authenticated Google Photos Album using the Library API, writes them to `images/`, and then shows them in a slideshow forever. There are instructions and a script (`run.sh`) for Linux to run the script on boot.

## Environment Setup
1. `python -m venv env` (or your environment manager of choice—you'll have to update `run.sh` if you use a different virtual environment or name)
2. `source env/bin/activate`
3. `pip install -r requirements.txt`

## Google Photos API Setup
On a separate computer (you'll need access to a browser/monitor/keyboard):
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or use an existing one
3. Enable the Google Photos Library API for your project
4. Create credentials (OAuth 2.0 Client ID):
   1. Go to APIs & Services > Credentials
   2. Click Create Credentials > OAuth Client ID.
   3. Download the credentials JSON file to this repo and rename it to `credentials.json`
5. `python photos_api.py` to go through the auth process, save the token pickle file, and determine the correct album id
6. Transfer `token.pickle` and `credentials.json` to the pi's `digital-frame` directory; transfer the album id string to the top of `main.py` on the pi.

## Running on Boot
More detailed instructions can be found in [this blog post](#).

These instructions are for Raspberry Pi OS Lite. You won't need to install and manually start up the display server if you install the full Raspberry Pi OS.

1. `sudo apt update && sudo apt install xserver-xorg openbox xinit python3-tk git-all`
2. Set up autologin:
	1. `sudo mkdir -p /etc/systemd/system/getty@tty1.service.d`
	2. `sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf`
	3. Add config (replace `user` with the appropriate user):
	```
		[Service] 
		ExecStart= 
		ExecStart=-/sbin/agetty --noclear --autologin user %I $TERM
	```
	4. `sudo systemctl daemon-reload`
	5. `sudo systemctl enable getty@tty1.service`
3. To execute `run.sh` on boot:
	- `crontab -e` and add: `@reboot /path/to/digital-frame/run.sh >> /path/to/digital-frame/logfile.log 2>&1` to the bottom


## Settings
You can update the duration each photo is shown and the background color at the top of `main.py`.