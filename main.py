"""
PiConsole

OVERVIEW:
A touch screen clock radio for the Pi that shows the time, weather
and plays Internet radio streams

REQUIREMENTS:
Only compatible with Python 3
Uses:
- Kivy for the touchscreen interface
- mpd and mpc for playing internet radio streams
-- mpd playlists are managed manually outside this application
- Weather Underground API to get weather information
- Openhab Python library (python-openhab) to get data from Openhab server
- pyalsaaudio for Alsa volume controls

NOTES:
All variables are hard-coded so file should not be shared without
first removing private info
"""

import os
# needed to stop icon downloaded from Weather Underground from flashing
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
import subprocess
import alsaaudio
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from time import strftime
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
from openhab import openHAB
from kivy.uix.popup import Popup

class PiConsoleApp(App):
	clock_time = StringProperty()
	clock_date = StringProperty()
	temp = StringProperty()
	temp_notes = StringProperty()
	conditions_image = StringProperty()
	weather_url = StringProperty()
	deg = '\u00b0'
	rm1_temp = StringProperty()
	rm2_temp = StringProperty()
	rm3_temp = StringProperty()
	a_time = StringProperty()
	a_image = StringProperty()
	a_temp = StringProperty()
	a_feelslike = StringProperty()
	b_time = StringProperty()
	b_image = StringProperty()
	b_temp = StringProperty()
	b_feelslike = StringProperty()
	c_time = StringProperty()
	c_image = StringProperty()
	c_temp = StringProperty()
	c_feelslike = StringProperty()
	d_time = StringProperty()
	d_image = StringProperty()
	d_temp = StringProperty()
	d_feelslike = StringProperty()
	radio_station = StringProperty()
	radio_song_artist = StringProperty()
	radio_song_title = StringProperty()

	def update_clock(self, *args):
		self.clock_time = strftime('[b]%H[/b]:%M:%S')
		self.clock_date = strftime('%a %d %b %Y')

	def got_conditions(self, req, result):

		self.conditions_image = \
			result['current_observation']['icon_url']

		temp_c = int(round(result['current_observation']['temp_c'],0))

		self.temp = str(temp_c) + "[sup]" + self.deg + "C [/sup]"

		feelslike = float(result['current_observation']['feelslike_c'])
		conditions = result['current_observation']['weather']

		self.temp_notes = "Feels like " + \
			str(int(round(feelslike,0))) + \
			self.deg + "\n" + conditions

			# Wunderground returns feelike as a string so we first need
			# to convert it to a float, round it and then convert it to
			# an int and then finally a string

	def got_forecast(self, req, result):

		try:
			self.a_time = result['hourly_forecast'][2]['FCTTIME']['civil']
			self.a_temp = \
				result['hourly_forecast'][2]['temp']['metric'] + self.deg
			self.a_image = result['hourly_forecast'][2]['icon_url']
			self.a_feelslike = "Feels like " + \
				result['hourly_forecast'][2]['feelslike']['metric'] + \
				self.deg

			self.b_time = result['hourly_forecast'][5]['FCTTIME']['civil']
			self.b_temp = \
				result['hourly_forecast'][5]['temp']['metric'] + self.deg
			self.b_image = result['hourly_forecast'][5]['icon_url']
			self.b_feelslike = "Feels like " + \
				result['hourly_forecast'][5]['feelslike']['metric'] + \
				self.deg

			self.c_time = result['hourly_forecast'][8]['FCTTIME']['civil']
			self.c_temp = \
				result['hourly_forecast'][8]['temp']['metric'] + self.deg
			self.c_image = result['hourly_forecast'][8]['icon_url']
			self.c_feelslike = "Feels like " + \
				result['hourly_forecast'][8]['feelslike']['metric'] + \
				self.deg

			self.d_time = result['hourly_forecast'][11]['FCTTIME']['civil']
			self.d_temp = \
				result['hourly_forecast'][11]['temp']['metric'] + self.deg
			self.d_image = result['hourly_forecast'][11]['icon_url']
			self.d_feelslike = "Feels like " + \
				result['hourly_forecast'][11]['feelslike']['metric'] + \
				self.deg

		except:
			self.a_time = ""
			self.a_temp = ""
			self.a_image= ""
			self.a_feelslike = ""

			self.b_time = ""
			self.b_temp = ""
			self.b_image= ""
			self.b_feelslike = ""

			self.c_time = ""
			self.c_temp = ""
			self.c_image= ""
			self.c_feelslike = ""

			self.d_time = ""
			self.d_temp = ""
			self.d_image= ""
			self.d_feelslike = ""

	def update_weather(self, *args):
		conditions_url = "http://api.wunderground.com/api/" + \
			"<enter your api key here>/geolookup/conditions/q/" + \
			"canada/Calgary.json"

		forecast_url = "http://api.wunderground.com/api/" + \
			"<enter your api key here>/geolookup/hourly/q/" + \
			"canada/Calgary.json"

		conditions_req = UrlRequest(conditions_url, \
			self.got_conditions)

		forecast_req = UrlRequest(forecast_url, \
			self.got_forecast)


	def get_openhab_data(self, *args):
		openhab_url = 'http://<enter address of openHAB server here>:8080/rest'

		try:
			openhab = openHAB(openhab_url)
			items = openhab.fetch_all_items()

			rm1 = round(items.get('RM1_Temperature').state,0)
			self.rm1_temp = "room1: " + \
				str(int(rm1)) + self.deg + "C"

			rm2 = round(items.get('RM2_Temperature').state,0)
			self.rm2_temp = "room2: " + \
				str(int(rm2)) + self.deg + "C"

			rm3 = items.get('RM3_Temperature').state
			self.rm3_temp = "room3: " + \
				str(int(round(rm3,0))) + self.deg + "C"
		except:
			self.rm1_temp = "room1: "
			self.rm2_temp = "room2: "
			self.rm3_temp = "room3: "

	def radio_play_stn_1(self):
		subprocess.check_output(["mpc", "play", "1"])
		self.radio_station = "[b]Stn 1[/b]"
		self.get_radio_song_info()
		Clock.schedule_interval(self.get_radio_song_info, 10)

	def radio_play_stn_2(self):
		subprocess.check_output(["mpc", "play", "2"])
		self.radio_station = "[b]Stn 2[/b]"
		self.get_radio_song_info()
		Clock.schedule_interval(self.get_radio_song_info, 10)

	def radio_play_stn_3(self):
		subprocess.check_output(["mpc", "play", "3"])
		self.radio_station = "[b]Stn 3[/b]"
		self.get_radio_song_info()
		Clock.schedule_interval(self.get_radio_song_info, 10)


	def stop_radio(self):
		subprocess.check_output(["mpc", "stop"])
		self.radio_station = ""
		self.radio_song_title = ""
		self.radio_song_artist = ""
		Clock.unschedule(self.get_radio_song_info)

	def radio_vol_up(self):
#		subprocess.check_output(["mpc", "volume", "+5"])
		m = alsaaudio.Mixer('PCM')
		current_volume = m.getvolume()
		if current_volume[0] < 95 :
#			print (current_volume[0])
			m.setvolume(current_volume[0] + 5)

	def radio_vol_down(self):
#		subprocess.check_output(["mpc", "volume", "-5"])
		m = alsaaudio.Mixer('PCM')
		current_volume = m.getvolume()
		if current_volume[0] > 10 :
#			print (current_volume[0])
			m.setvolume(current_volume[0] - 5)

	def get_radio_song_info(self, *args):
		mpc_current = \
			str(subprocess.check_output(["mpc", "current"]))

		# remove trailing characters in string returned by mpc
		mpc_current = mpc_current[:-3]

		# remove leading characters in string returned by mpc
		mpc_current = mpc_current[2:]

		# this check is needed because mpc current does not return
		# station name when plaving Virgin stream
		if ":" in mpc_current:
			try:
				song_info = mpc_current.split(":")[1]
				song_artist = song_info.split(" - ")[0]
				# remove leading space from artist/song string
				self.radio_song_artist = song_artist[1:]
				self.radio_song_title = song_info.split(" - ")[1]
			except IndexError:
				self.radio_song_artist = ""
				self.radio_song_title = ""
		else:
			try:
				song_info = mpc_current
				self.radio_song_artist = song_info.split(" - ")[0]
				self.radio_song_title = song_info.split(" - ")[1]
			except IndexError:
				self.radio_song_artist = ""
				self.radio_song_title = ""

	def build(self):

		Window.size = (800, 480)
		Clock.schedule_interval(self.update_clock, 1.0 / 60.0)
		Clock.schedule_once(self.update_weather)
		Clock.schedule_interval(self.update_weather, 1800)
		Clock.schedule_once(self.get_openhab_data)
		Clock.schedule_interval(self.get_openhab_data, 600)

if __name__ == '__main__':

	PiConsoleApp().run()
