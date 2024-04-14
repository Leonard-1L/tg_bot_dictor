import telebot
from telebot.types import Message
from gpt import *
from database import *
from config import *

bot = telebot.TeleBot(token=BOT_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs.txt",
    filemode="w"
)

create_table("speech_kit.db")


@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {message.from_user.username} с ID {message.from_user.id} присоеденился к нам!")
    bot.send_message(user_id, f"Привет, {message.from_user.username}\n"
                              f"Я бот-диктор, озвучу почти всё, что ты мне напишешь.\n"
                              f"Используй команду /tts, а затем пришли нужный текст для озвучки.\n"
                              f"Если на каком-то моменте ты не понял, то пропиши /help. Там подробно расписано, что делать.")


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщеним текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)


def tts(message):
    user_id = message.from_user.id
    text = message.text

    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return

    logging.info(f"Пользователь {message.from_user.username} с ID {message.from_user.id} попросил озвучить '{text}'")

    text_symbol = is_tts_symbol_limit(message, text)

    if text_symbol is None:
        return

    insert_row(user_id, text, text_symbol)

    status, content = make_voice(text)

    if status:
        bot.send_voice(user_id, content)
        count_all_simvols_in_file()
        logging.info("Запись успешно отправлена.")
    else:
        bot.send_message(user_id, content)


def is_tts_symbol_limit(message, text):
    user_id = message.from_user.id
    text_symbols = len(text)

    all_symbols = count_all_symbol(user_id) + text_symbols
    logging.info(
        f"Символов было потрачено на запросе {text_symbols}. Всего было потрачено {all_symbols}. Осталось символов: {MAX_USER_TTS_SYMBOLS - all_symbols}")
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        bot.send_message(user_id, msg)
        return None

    if text_symbols >= MAX_REQUESTS_SYMBOLS:
        msg = f"Превышен лимит SpeechKit TTS на запрос {MAX_REQUESTS_SYMBOLS}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(text)


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    logging.info(f"Пользователь {message.from_user.username} с ID {message.from_user.id} запросил помощь.")
    bot.send_message(message.from_user.id, "Чтобы бот озвучил текст вы должны сперва прописать команду /tts.\n"
                                           "Затем расставить знаки ударения, паузы и акценты если это требуется.\n"
                                           f"Вскоре, если ваш текст меньше {MAX_REQUESTS_SYMBOLS} символов и вы потратили всего меньше {MAX_USER_TTS_SYMBOLS} символов, то бот пришлет вам аудио в течении нескольки секунд.\n"
                                           "Отсылаю язык синтеза:")
    with open("help_media/sintes_lang.png", "rb") as foto:
        bot.send_photo(message.from_user.id, foto)


@bot.message_handler(commands=['_logs_'])
def send_logs(message: Message):
    logging.info(f'{message.from_user.username} с ID {message.from_user.id} запросил логи')
    bot.send_document(message.from_user.id, 'logs.txt')


@bot.message_handler()
def else_message(message: Message):
    bot.reply_to(message=message,
                 text="Извините, но я вас не распонял. Удостоверьтесь, что вы следовали инструкции. Чтобы ее просмотреть - пропишите /help.")


if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.infinity_polling(none_stop=True, timeout=130)
