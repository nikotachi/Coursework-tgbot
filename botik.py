#THIS CODE IS FOR BOT("Обслуживание ПК")



#import libraries
import sqlite3
import telebot
from telebot import types

#our bot
bot = telebot.TeleBot("7801748981:AAHsPyi_glrbCRHtkDID4BuUyOKuSXuCFCk")
name = None
number = None
adress = None

#connect базу данных
conn = sqlite3.connect('user3.db')
cur = conn.cursor()

#на случай, если надо почистить базу данных
#cur.execute("DROP TABLE IF EXISTS users")

cur.execute("CREATE TABLE IF NOT EXISTS users (id varchar(50), name varchar(50), number varchar(50), adress varchar(50), remont varchar (50))")

keyboard = types.ReplyKeyboardMarkup()

def button_answer(message):
    bot.send_message()


#дальше начинаются команды для работы функционала
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('user3.db')
    cur = conn.cursor()

    #создаем столбики
    cur.execute('''SELECT * FROM users WHERE id='%s' ''' % str(message.chat.id))
    user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    #следующие строчки нужны для проверки наличия пользователя в БД, чтобы не регистрировать его второй раз
    if user is None:
        bot.send_message(message.chat.id, 'Здравствуйте, давайте регистрироваться! Введите свое Фамилию Имя',reply_markup=keyboard)
        bot.register_next_step_handler(message, user_name)
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы", reply_markup=keyboard)



def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, user_number)

def user_number(message):
    global number
    number = message.text.strip()
    bot.send_message(message.chat.id, 'Напишите адрес магазина, в котором вы купили ПК')
    bot.register_next_step_handler(message, user_adress)

def user_adress(message):
    global adress
    adress = message.text.strip()
    bot.send_message(message.chat.id, 'Опишите вашу проблему')
    bot.register_next_step_handler(message, user_remont, message.chat.id)

def user_remont(message, id):
    remont = message.text.strip()

    conn = sqlite3.connect('user3.db')
    cur = conn.cursor()


    #заполняем столбцы
    cur.execute('''INSERT INTO users (id, name, number, adress, remont) VALUES ('%s', '%s', '%s', '%s', '%s')''' % (id, name, number, adress, remont))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Вы заполнили данные, введите /vhod для дальнейших действий')


@bot.callback_query_handler(func=lambda call: call.data == 'open_cabinet')
def callback(call):
    conn = sqlite3.connect('user3.db')
    cur = conn.cursor()

    cur.execute('''SELECT * FROM users WHERE id='%s' ''' % str(call.message.chat.id))
    users = cur.fetchone()
    info = f"Фамилия Имя: {users[1]}, номер телефона: {users[2]}\n"
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

@bot.callback_query_handler(func=lambda call: call.data == 'open_zayavka')
def callbacks(call):
    conn = sqlite3.connect('user3.db')
    cur = conn.cursor()

    cur.execute('''SELECT * FROM users WHERE id='%s' ''' % str(call.message.chat.id))
    users = cur.fetchone()
    info1 = f"Адрес магазина: {users[3]}, ваша заявка: {users[4]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info1)

@bot.callback_query_handler(func=lambda call: call.data == 'open_status')
def callbacking(call):
    bot.send_message(call.message.chat.id, 'Ожидайте ответа в течение 5 дней от отправки заявки')

@bot.message_handler(commands=['vhod'])
def send_wel(message):
    conn = sqlite3.connect('user3.db')
    cur = conn.cursor()


    #начинаем обращаться к нашим данным, чтобы была возможность их вывести
    cur.execute('''SELECT * FROM users WHERE id='%s' ''' % str(message.chat.id))
    exist = cur.fetchone()
    if exist is not None:  # если человека с таким id нету в бд
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Личный кабинет", callback_data="open_cabinet"))
        markup.add(telebot.types.InlineKeyboardButton("Мои заявки", callback_data='open_zayavka'))
        markup.add(telebot.types.InlineKeyboardButton("Узнать статус заявки", callback_data='open_status'))
        bot.send_message(message.chat.id, "Здравствуйте, выберете дальнейшее действие", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нету аккаунта. Введите /start для регистрации")

bot.infinity_polling()