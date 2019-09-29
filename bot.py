import logging
import os

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from config import Config
from kuda_go import KudaGoApi, MetropolisAPI

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

c = Config()
kudago_api = KudaGoApi()
metropolis_api = MetropolisAPI()


def start(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(f'{c.STATIC_DIR}/nyan_cat.jpg', 'rb'))
    context.bot.send_message(chat_id=update.message.chat_id, text="Приффки-привиффки! Я вафельно-походный бот")


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def films(update, context):
    films_list = kudago_api.get_recent_films()
    for film in films_list:
        context.bot.send_photo(chat_id=update.message.chat_id,
                               caption=f'<b>{film.title}</b>\n{film.description}',
                               photo=film.image_url,
                               parse_mode='HTML')


def metropolis(update, context):
    films_list = metropolis_api.get_recent_films()
    for film in films_list:
        buttons_in_raw = 4
        session_buttons = [
            telegram.InlineKeyboardButton(text=session.time,
                                          url=film.description_href)
            for session in film.schedule
        ]
        inline_keyboard = [session_buttons[i:i + buttons_in_raw] for i in range(0, len(session_buttons), buttons_in_raw)]
        reply_markup = telegram.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        caption = f'<b>{film.title}</b>\n{film.description}\n\n<b>Сеансы:</b>\n'
        context.bot.send_photo(chat_id=update.message.chat_id,
                               caption=caption,
                               photo=film.image_url,
                               parse_mode='HTML',
                               reply_markup=reply_markup)


def pidr(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Ты пидор")


def main():
    PORT = os.environ.get('PORT')
    NAME = 'blooming-wave-39288'
    updater = Updater(
        token=c.TOKEN,
        use_context=True,
        request_kwargs={'read_timeout': 30, 'connect_timeout': 7},

    )
    dispatcher = updater.dispatcher

    # Handlers
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text, echo)
    films_handler = CommandHandler('films', films)
    pidr_handler = CommandHandler('pidr', pidr)
    metropolis_handler = CommandHandler('metropolis', metropolis)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(films_handler)
    dispatcher.add_handler(pidr_handler)
    dispatcher.add_handler(metropolis_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=c.TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, c.TOKEN))
    updater.idle()

    updater.idle()


if __name__ == "__main__":
    main()
