import logging
import sqlite3
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs.txt",
    filemode="w"
)


def create_table(db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                tts_symbols INTEGER)
            ''')
            conn.commit()
    except Exception as e:
        logging.error(f"Error: {e} in func create_table")


def insert_row(user_id, message, tts_symbols, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)''',
                           (user_id, message, tts_symbols))
            conn.commit()
    except Exception as e:
        logging.error(f"Error: {e} in func insert_row")


def count_all_symbol(user_id, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''',
                           (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                return data[0]
            else:
                return 0
    except Exception as e:
        logging.error(f"Error: {e} in func count_all_symbol")


def count_all_simvols_in_file(column_name="tts_symbols", table_name="messages", db_name="speech_kit.db"):
    """Функция для того, чтобы контролировать кол-во всего затраченных токенов"""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            query = f"SELECT SUM({column_name}) FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchone()[0]

        with open("count_tokens.txt", 'a') as file:
            file.write(
                f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))} - затрачено всего токенов {result}" + '\n')
    except Exception as e:
        logging.error(f"Error: {e} in func count_all_simvols_in_file")
