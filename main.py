import bs4
import telebot
import requests
from telebot import types
import dz
from menu import Menu, Users
import pygame
import menu
import random

value1 = ''
old_value = ''

keyboard1 = telebot.types.InlineKeyboardMarkup()
keyboard1.row(telebot.types.InlineKeyboardButton('00', callback_data='00'),
              telebot.types.InlineKeyboardButton('C', callback_data='C'),
              telebot.types.InlineKeyboardButton('<=', callback_data='<='),
              telebot.types.InlineKeyboardButton('/', callback_data='/'))
keyboard1.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
              telebot.types.InlineKeyboardButton('8', callback_data='8'),
              telebot.types.InlineKeyboardButton('9', callback_data='9'),
              telebot.types.InlineKeyboardButton('*', callback_data='*'))
keyboard1.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
              telebot.types.InlineKeyboardButton('5', callback_data='5'),
              telebot.types.InlineKeyboardButton('6', callback_data='6'),
              telebot.types.InlineKeyboardButton('-', callback_data='-'))
keyboard1.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
              telebot.types.InlineKeyboardButton('2', callback_data='2'),
              telebot.types.InlineKeyboardButton('3', callback_data='3'),
              telebot.types.InlineKeyboardButton('+', callback_data='+'))
keyboard1.row(telebot.types.InlineKeyboardButton('**', callback_data='**'),
              telebot.types.InlineKeyboardButton('0', callback_data='0'),
              telebot.types.InlineKeyboardButton(',', callback_data='.'),
              telebot.types.InlineKeyboardButton('=', callback_data='='))
keyboard1.row(telebot.types.InlineKeyboardButton('%', callback_data='%'),
              telebot.types.InlineKeyboardButton('//', callback_data='//'),
              telebot.types.InlineKeyboardButton('(', callback_data='('),
              telebot.types.InlineKeyboardButton(')', callback_data=')'))

bot = telebot.TeleBot('5008394487:AAFnUArSitfnYoocKsustnBMTb41NY2YjGE')  # Создаем экземпляр бота @Ivanov_Ivan_1MD19_bot


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


@bot.message_handler(commands=['get_info', 'info'])
def info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Хотите узнать больше о проектах автора и его соц. сетях?',
                     reply_markup=markup_inline
                     )


@bot.message_handler(content_types=['text'])
def bot_message(message):
    chat_id = message.chat.id
    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])
    result = goto_menu(chat_id, message.text)

    if result == True:
        return

    cur_menu = Menu.getCurMenu(chat_id)

    if cur_menu != None and message.text in cur_menu.buttons:
        if message.text == '1 Задание':
            dz.dz1(bot, chat_id)
        elif message.text == '2 Задание':
            dz.dz2(bot, chat_id)
        elif message.text == '3 Задание':
            dz.dz3(bot, chat_id, message)
        elif message.text == '4 Задание':
            dz.dz4(bot, chat_id, message)
        elif message.text == '5 Задание':
            dz.dz5(bot, chat_id, message)
        elif message.text == '6 Задание':
            dz.dz6(bot, chat_id, message)
        elif message.text == '7 Задание':
            dz.dz7(bot, chat_id, message)
        elif message.text == '8 Задание':
            dz.dz8(bot, chat_id, message)
        elif message.text == '9 Задание':
            dz.dz9(bot, chat_id, message)
        elif message.text == '10 Задание':
            dz.dz10(bot, chat_id, message)
        # elif message.text =='Статистика XO':
        #     xl.stat_give(bot,chat_id,message)
        elif message.text == 'О Авторе':
            markup_inline = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
            item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
            markup_inline.add(item_yes, item_no)
            bot.send_message(chat_id, 'Хотите узнать больше о проектах автора и его соц. сетях?',
                             reply_markup=markup_inline
                             )

        elif message.text == 'Анекдот':
            # bot.send_message(chat_id, text=get_anekdot())
            bot.send_message(chat_id, text=get_anekdot())
        elif message.text == "Создать ник":
            bot.send_message(message.chat.id, text=get_nickname())
        elif message.text == "Показать лисичку":
            contents = requests.get('https://randomfox.ca/floof').json()
            urlCAT = contents['image']
            bot.send_photo(message.chat.id, photo=urlCAT)
        elif message.text == "Калькулятор":
            global value1
            if value1 == '':
                bot.send_message(message.from_user.id, '0', reply_markup=keyboard1)
            else:
                bot.send_message(message.from_user.id, value1, reply_markup=keyboard1)
        elif message.text == "Старт":
            bot.register_next_step_handler(message, reggame)
        elif message.text == "Карту!":
            game21 = pygame.getGame(chat_id)
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                pygame.stopGame(chat_id)
                goto_menu(chat_id, "Выход")
                return

        elif message.text == "Стоп!":
            pygame.stopGame(chat_id)
            goto_menu(chat_id, "Выход")
            return


def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""


# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = menu.Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = menu.Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = menu.Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = pygame.newGame(chat_id, pygame.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = pygame.newGame(chat_id, pygame.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game,
                           parse_mode='HTML')

        return True
    else:
        return False


def get_nickname():
    array_names = []
    req_names = requests.get("https://ru.nickfinder.com")
    soup = bs4.BeautifulSoup(req_names.text, "html.parser")
    result_find = soup.findAll(class_='one_generated_variant vt_df_bg')
    for result in result_find:
        array_names.append(result.getText())
    return array_names[0]


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


@bot.callback_query_handler(func=lambda call: True)
def calllback_fun(query):
    global value1, old_value
    data = query.data

    if data == 'no':
        pass
    elif data =='<=':
        value1 = value1[:-1]
    elif data == 'C':
        value1 = '0'
    elif value1 =='0':
        value1 = value1[:-1]
    elif data == '=':
        value1 = str(eval(value1))
    else:
        value1 += data

    if value1 != old_value:
        if value1 == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                  reply_markup=keyboard1)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value1,
                                  reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: True)
def reggame(message):
    option = ['Камень', 'Ножницы', 'Бумага']
    global game
    global value
    value = random.choice(option)
    game = message.text
    if game == 'Камень':
        if value == 'Камень':
            bot.send_message(message.chat.id, 'Ничья')
        if value == 'Ножницы':
            bot.send_message(message.chat.id, 'Вы победили, я поставил ножницы')
        if value == 'Бумага':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставил бумагу')
    if game == 'Ножницы':
        if value == 'Камень':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставил камень')
        if value == 'Ножницы':
            bot.send_message(message.chat.id, 'Ничья')
        if value == 'Бумага':
            bot.send_message(message.chat.id, 'Вы выиграли , я поставил бумагу')
    if game == 'Бумага':
        if value == 'Камень':
            bot.send_message(message.chat.id, 'Вы выиграли , я поставил камень')
        if value == 'Ножницы':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставил ножницы')
        if value == 'Бумага':
            bot.send_message(message.chat.id, 'Ничья')


# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()
