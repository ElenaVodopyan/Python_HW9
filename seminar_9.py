import telebot
import random
from telebot import types

game_started = False
r_number = None

bot = telebot.TeleBot("6261930244:AAGBjccmLsnBJ2ossQWZd9MUsGPYX3hOWXE")

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('/играть')
markup.add(itembtn1)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.send_message(message.from_user.id, 'Как дела?')
	bot.send_message(message.from_user.id, "Нажмите 'Играть':", reply_markup=markup)

@bot.message_handler(commands=['играть'])
def play_game(message):
	global game_started 
	global r_number

	if not game_started:
		game_started = True
		r_number = random.randint(1, 1000)
		bot.reply_to(message, 'Загадано число от 1 до 1000. Отгадай его!')
		return
	else:
		bot.reply_to(message, 'Игра уже началась! Повтори попытку.')	 
		return

@bot.message_handler(content_types=['text'])
def read_text_commands(message):	
	global game_started
	global r_number

	data = open('message.txt', 'a', encoding='utf-8')
	text = f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.id}: {message.text}'
	data.writelines(f'{text}\n')
	data.close

	if game_started:
		if message.text.isdigit():
			number = int(message.text)
			if number > r_number:
				bot.reply_to(message, 'Моё число меньше')
			elif number < r_number:
				bot.reply_to(message, 'Моё число больше')
			elif number == r_number:
				game_started = False
				bot.reply_to(message, f'Ты крутышка! Угадал! Я загадала число {r_number}')
		else:
			bot.reply_to(message, 'Ничего не понял...')
			return

bot.infinity_polling()
					
					

	
		





