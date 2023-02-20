import telebot
import random
from telebot import types

game_started = False
r_number = None
steps_count = 0

bot = telebot.TeleBot("6261930244:AAGBjccmLsnBJ2ossQWZd9MUsGPYX3hOWXE")

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('/играть')
itembtn2 = types.KeyboardButton('/вычислить')
markup.add(itembtn1, itembtn2)

def show_menu(chat_id):
	bot.send_message(chat_id, "Выберите действие':", reply_markup=markup)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.send_message(message.from_user.id, 'Как дела?')
	show_menu(message.from_user.id)

@bot.message_handler(commands=['играть'])
def play_game(message):
	global game_started 
	global r_number
	global steps_count 
	if not game_started:
		steps_count = 0
		game_started = True
		r_number = random.randint(1, 1000)
		bot.reply_to(message, 'Загадано число от 1 до 1000. Отгадай его!')
		return
	else:
		bot.reply_to(message, 'Игра уже началась! Повтори попытку.')	 
		return

@bot.message_handler(commands=['вычислить'])
def calculation(message):
	bot.reply_to(message, 'Введите выражение')
	bot.register_next_step_handler(message, calculate)	

@bot.message_handler(content_types=['text'])
def read_text_commands(message):	
	global game_started
	global r_number
	global steps_count 

	data = open('message.txt', 'a', encoding='utf-8')
	text = f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.id}: {message.text}'
	data.writelines(f'{text}\n')
	data.close

	if game_started:
		if message.text.isdigit():
			number = int(message.text)
			steps_count += 1
			if number > r_number:
				bot.reply_to(message, 'Моё число меньше')
			elif number < r_number:
				bot.reply_to(message, 'Моё число больше')
			elif number == r_number:
				game_started = False
				bot.reply_to(message, f'Ты крутышка! Угадал за {steps_count} попыток! Я загадала число {r_number}')
				show_menu(message.from_user.id)
		else:
			bot.reply_to(message, 'Ничего не понял...')
			return


def calculate(message):
	try:
		bot.reply_to(message, f'Ответ: {eval(message.text)}')		
	except SyntaxError:
		bot.reply_to(message, f'Вы ввели неверное выражение')
	
	show_menu(message.from_user.id)


bot.infinity_polling()
					
					

	
		





