import telebot
import wikipediaapi
import sqlite3
import wikipedia
import get_links
import database


conn = sqlite3.connect('wiki_bot.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS favorites
                (user_id INTEGER, title TEXT, url TEXT)''')
special_url = ''
special_title = ''
wiki = wikipediaapi.Wikipedia('ru')
bot = telebot.TeleBot("6283184666:AAFOrIwO5KBXqFsO3YZDx0275F2Ponhy2wg")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    random_button = telebot.types.KeyboardButton('Случайная статья')
    last_five_geography_pages = telebot.types.KeyboardButton('География')
    last_five_since_pages = telebot.types.KeyboardButton('Наука')
    last_five_sport_pages = telebot.types.KeyboardButton('Спорт')
    last_five_games_pages = telebot.types.KeyboardButton('История')
    last_five_pages = telebot.types.KeyboardButton('Последние 5 статей')
    favorites_button = telebot.types.KeyboardButton('Избранное')
    add_favorites_button = telebot.types.KeyboardButton('Добавить в избранное')
    markup.row(random_button, last_five_pages, last_five_geography_pages, last_five_since_pages, )
    markup.row(last_five_sport_pages, last_five_games_pages, favorites_button, add_favorites_button, )
    bot.reply_to(message,
                 "Привет! Я бот, который может искать информацию в Википедии. Просто напишите мне ваш запрос, "
                 "и я постараюсь найти соответствующую статью.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.startswith('Удалить из избранного: '))
def remove_from_favorites(message):
    # Разделить сообщение на команду и ссылку на статью
    command, link = message.text.split(': ')
    conn = sqlite3.connect('wiki_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM favorites WHERE user_id=(?) and url=(?)", (message.chat.id, link))
        conn.commit()
        bot.reply_to(message, f'Статья {link} удалена из избранного.')
    except sqlite3.Error as e:
        print('Ошибка при выполнении запроса:', e)
        bot.reply_to(message, f'Произошла ошибка при удалении статьи {link}.')


@bot.message_handler(func=lambda message: True)
def search_wiki(message):
    global special_url
    global special_title
    try:
        if message.text == 'Случайная статья':
            random_article = get_links.get_random_article()
            text = random_article[0] + ": " + random_article[1]
            special_title = random_article[0]
            special_url = random_article[1]
            bot.reply_to(message, text)
        elif message.text == "Последние 5 статей":
            recent_changes = get_links.get_five_pages()
            for change in recent_changes:
                title = change["title"]
                link = "https://ru.wikipedia.org/wiki/" + title.replace(" ", "_")
                bot.send_message(message.chat.id, title + '\n' + link)
        elif message.text == 'География':
            g_pages = get_links.get_five_theme_pages('география')
            text = 'Статьи по вашему запросу:\n'
            for page in g_pages:
                wiki_page = wikipedia.page(page)
                text += wiki_page.title + ':' + wiki_page.url + '\n'
            bot.send_message(message.chat.id, text)
        elif message.text == 'География':
            g_pages = get_links.get_five_theme_pages('география')
            text = 'Статьи по вашему запросу:\n'
            for page in g_pages:
                wiki_page = wikipedia.page(page)
                text += wiki_page.title + ':' + wiki_page.url + '\n'
            bot.send_message(message.chat.id, text)
        elif message.text == 'Наука':
            g_pages = get_links.get_five_theme_pages('наука')
            text = 'Статьи по вашему запросу:\n'
            for page in g_pages:
                wiki_page = wikipedia.page(page)
                text += wiki_page.title + ':' + wiki_page.url + '\n'
            bot.send_message(message.chat.id, text)
        elif message.text == 'Спорт':
            g_pages = get_links.get_five_theme_pages('спорт')
            text = 'Статьи по вашему запросу:\n'
            for page in g_pages:
                wiki_page = wikipedia.page(page)
                text += wiki_page.title + ':' + wiki_page.url + '\n'
            bot.send_message(message.chat.id, text)
        elif message.text == 'История':
            g_pages = get_links.get_five_theme_pages('история')
            text = 'Статьи по вашему запросу:\n'
            for page in g_pages:
                wiki_page = wikipedia.page(page)
                text += wiki_page.title + ':' + wiki_page.url + '\n'
            bot.send_message(message.chat.id, text)
        elif message.text == 'Избранное':
            user_id = message.from_user.id
            url_articles = database.get_favorites(user_id)
            # Отправляем список статей в чат
            if len(url_articles) > 0:
                text = 'Ваши избранные статьи:\n\n'
                for i in url_articles:
                    text += f'• {i[0]}: {i[1]}\n'
            else:
                text = 'В вашем списке избранных статей пока нет ни одной статьи.'
            bot.reply_to(message, text)
        elif message.text == 'Добавить в избранное':
            database.add_to_favorites(message.chat.id, special_title, special_url)
            bot.reply_to(message, "Статья добавленна в избранное: " + special_url)
        else:
            query = message.text
            page = wiki.page(query)
            if page.exists():
                result = page.fullurl
                title = page.title
                bot.reply_to(message, "Статья по вашему запросу:\n" + result)
                special_url = result
                special_title = title
            else:
                bot.reply_to(message, "К сожалению, я не смог найти информацию по вашему запросу.")
    except:
        print("error")
        bot.reply_to(message, "К сожалению, я не смог найти информацию по вашему запросу.")


bot.polling()
