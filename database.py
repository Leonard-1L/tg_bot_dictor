import logging
import sqlite3

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
