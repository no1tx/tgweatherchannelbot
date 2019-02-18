# -*- coding: utf-8 -*-
from metar import Metar
from apscheduler.schedulers.blocking import BlockingScheduler
from metar.Metar import Metar
import requests
import json
import config
import telebot

bot = telebot.TeleBot(config.token)
code = config.code
channel = config.channel
sendtimestamp = ''

def fetch_and_decode_metar(code):
	global decoded_data
	link = 'http://metartaf.ru/' + code + '.json'
	print(f'Send request to {link}')
	response = requests.get(link)
	parsed_response = json.loads(response.text)
	print('JSON load')
	city = parsed_response["name"]
	metar_data = parsed_response["metar"]
	print(f'METAR DATA: {metar_data}')
	metar_data = metar_data.split('\n')
	metar_data = metar_data[1]
	decoded_data = Metar(metar_data)

def send():
	if timestamp != sendtimestamp:
		bot.send_message(chat_id=channel, text=message)
		sendtimestamp = timestamp
	else:
		print('Message is same, stop')

def create_message():
	global message
	global timestamp
	fetch_and_decode_metar(code)
	timestamp = str(decoded_data.time)
	time = 'Время измерения: ' + str(decoded_data.time) + '\n'
	if not decoded_data.present_weather():
		weather = 'Погода: clear\n'
	else:
		weather = 'Погода: ' + decoded_data.present_weather() + '\n'
	temp = 'Температура: ' + str(decoded_data.temp) + '\n'
	dew_point = 'Точка росы:' + str(decoded_data.dewpt) + '\n'
	wind = 'Ветер: ' + decoded_data.wind(units="KMH") + '\n'
	visibility = 'Видимость: ' + decoded_data.visibility() + '\n'
	pressure = 'Давление: ' + str(decoded_data.press) + '\n'
	sky = 'Небо: ' + decoded_data.sky_conditions() + '\n'
	message = time + weather + temp + wind + dew_point + visibility + pressure + sky + 'Источник данных: metartaf.ru'

def create_schedule():
	scheduler = BlockingScheduler()
	scheduler.add_job(send, 'interval', hours=1)
	scheduler.start()

fetch_and_decode_metar(code) #for initial starting
create_schedule()
