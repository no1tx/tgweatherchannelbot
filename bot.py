# -*- coding: utf-8 -*-
from metar import Metar
from apscheduler.schedulers.background import BackgroundScheduler
from metar.Metar import Metar
import requests
import json
import config
import telebot

bot = telebot.TeleBot(config.token)
code = config.code


def fetch_and_decode_metar(code):
	global decoded_data
	link = 'http://metartaf.ru/' + code + '.json'
	print(f'Send request to {link}')
	response = requests.get(link)
	parsed_response = json.loads(response.text)
	city = parsed_response["name"]
	metar_data = parsed_response["metar"]
	print(f'METAR DATA: {metar_data}')
	metar_data = metar_data.split('\n')
	metar_data = metar_data[1]
	decoded_data = Metar.Metar(metar_data)

def sendh():
	fetch_and_decode_metar(code)
	time = 'Время измерения: ' + decoded_data.time + '\n'
	weather = 'Погода: ' + decoded_data.present_weather() + '\n'
	temp = 'Температура: ' + decoded_data.temp + '\n'
	wind = 'Ветер: ' + decoded_data.wind(units="KMH") + '\n'
	bot.send_message(chat_id='@arkhangelsk_talagi_weather', text=time)



scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(sendh, min(1-59))