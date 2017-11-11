A touchscreen clock radio for the Pi that shows the time, weather and plays Internet radio streams

Check out my blog for more info: http://rajiv.rsshah.net/2017/11/pi-touch.html


REQUIREMENTS:
Only compatible with Python 3

DEPENDENCIES:
- Kivy for the touchscreen interface
- mpd and mpc for playing internet radio streams
- mpd playlists are managed manually outside this application
- Weather Underground API to get weather information
- Openhab Python library (python-openhab) to get data from Openhab server
- pyalsaaudio for Alsa volume controls

NOTES:
All variables are hard-coded so file should not be shared without first removing private info
