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
    context.bot.send_photo(chat_id=update.message.chat_id,
                               caption="<b>Глубокая глотка</b>\nГлавная героиня (Линда Лавлейс) не в состоянии получить сексуальное удовлетворение. Специалист (Гарри Римс), к которому она обращается со своими проблемами, выясняет причину, которая состоит в том, что её клитор находится глубоко в горле. Обрадованная поставленным диагнозом, Линда осваивает специфическую технику орального секса, которую в фильме именуют «глубокой глоткой», и «оттачивает» её на различных партнёрах, пока не находит себе наиболее подходящего с нужным размером члена.",
                               photo="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Deep_throat_PD_poster_%28restored%29.png/546px-Deep_throat_PD_poster_%28restored%29.png",
                               parse_mode='HTML')


def metropolis(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                               caption="<b>Глубокая глотка</b>\nГлавная героиня (Линда Лавлейс) не в состоянии получить сексуальное удовлетворение. Специалист (Гарри Римс), к которому она обращается со своими проблемами, выясняет причину, которая состоит в том, что её клитор находится глубоко в горле. Обрадованная поставленным диагнозом, Линда осваивает специфическую технику орального секса, которую в фильме именуют «глубокой глоткой», и «оттачивает» её на различных партнёрах, пока не находит себе наиболее подходящего с нужным размером члена.",
                               photo="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Deep_throat_PD_poster_%28restored%29.png/546px-Deep_throat_PD_poster_%28restored%29.png",
                               parse_mode='HTML')


def pidr(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Ты пидор")


def main():
    PORT = os.environ.get('PORT')
    NAME = 'wafflexxx'
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
