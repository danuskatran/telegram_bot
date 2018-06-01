import logging
import re
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram.ext import CommandHandler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TOKEN = "506052464:AAFH_JpUloAOURCmKVqgQ_kY8ZZE9qvjifo"

def callback_minute(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text='One message every minute')
    job_queue.run_repeating(callback_minute, interval=60, first=0)

def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

def link_deleter(bot, update):
    # delete messages with urls
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       update.message.text.lower())

    #admins = get_admin_ids()

    for url in urls:    # for url, admin in urls, admins:
        if url not in ["https://etherscan.io/address/brickblock-ico.eth", "https://www.brickblock.io/"]: #or admin not in admins:
             bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
             bot.send_message(chat_id=update.message.chat_id, text="No links are allowed: Warning.")
    return urls
    

def address_deleter(bot, update):
    # delete ETH addresses except for ours
    addresses = re.findall('^0x([A-Fa-f0-9]{40})$', update.message.text.lower())
    #admins = get_admin_ids()

    for address in addresses:
        if address != '0xC7F4ed68592327Aa2755b320c353B1aF715020DD':
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            bot.send_message(chat_id=update.message.chat_id, text="Warning, do not send your ETH addresses!")
    return addresses

def welcome(bot, update):
    if update.message.new_chat_members:
        bot.send_message(chat_id=update.message.chat_id, text="Welcome " + update.message.new_chat_members[0].first_name + " ")

def main():
    updater = Updater(TOKEN)
    j = updater.job_queue
    dispatcher = updater.dispatcher
    timer_handler = CommandHandler('timer', callback_minute, pass_job_queue=True)
    dispatcher.add_handler(timer_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, link_deleter))
    dispatcher.add_handler(MessageHandler(Filters.text, address_deleter))
    dispatcher.add_handler(MessageHandler(Filters.status_update, welcome))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
