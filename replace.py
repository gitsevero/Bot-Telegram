import telegram
import schedule
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Token do seu bot gerado pelo BotFather
TOKEN = ""

# Inicializa o bot
bot = telegram.Bot(token=TOKEN)


# Define a função que será executada quando o comando /start for enviado ao bot
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Olá! Estou aqui para ajudar."
    )


# Define a função que será executada quando uma nova mensagem for enviada ao grupo
def mensagem_grupo(update, context):
    # Obtém o texto da mensagem
    message_text = update.message.text

    # Envia a mensagem para o chat do usuário
    context.bot.send_message(chat_id="", text=message_text)


# Cria um objeto Updater e adiciona os handlers para os comandos e mensagens
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, mensagem_grupo))


# Agendamento da busca por atualizações do chat
def check_updates(bot, chat_id, context):
    messages = bot.get_updates()[-10:]
    for message in messages:
        bot.send_message(chat_id=chat_id, text=message.message.text)


schedule.every(10).seconds.do(check_updates, bot=bot, chat_id="", context=dispatcher)

# Inicia o bot
updater.start_polling()

# Loop de execução do agendamento
while True:
    schedule.run_pending()
    time.sleep(1)
