import sqlite3


def add_to_favorites(user_id, title, url):
    conn = sqlite3.connect('wiki_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO favorites VALUES (?, ?, ?)", (user_id, title, url))
        conn.commit()
    except sqlite3.Error as e:
        print('Ошибка при выполнении запроса:', e)


def get_favorites(user_id):
    conn = sqlite3.connect('wiki_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT title, url FROM favorites WHERE user_id=?", (user_id,))
    except sqlite3.Error as e:
        print('Ошибка при выполнении запроса:', e)
    rows = cursor.fetchall()
    # Формируем список статей
    articles = [row[0] for row in rows]
    urls = [row[1] for row in rows]
    all = tuple(zip(articles, urls))
    return all