from chatapp import ChatApp
from dotenv import load_dotenv, find_dotenv
import os
import telebot
from datetime import datetime, timedelta
current_time = datetime.now()
one_hour_before = current_time - timedelta(hours=1)

load_dotenv(find_dotenv("data.env"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

chatbot = ChatApp()

username = None


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    global username
    reply = f"Thank you, {message.from_user.first_name}! Your username {username} has been recorded. You can start chatting now."
    user_id = message.from_user.id
    username = str(user_id)

    if chatbot.get_user(username) is None:
        chatbot.response_generator.store_complete_data(username, message.text, reply)
        bot.reply_to(message, reply)
    else:

        if message.text == "report":
            bot.reply_to(message, chatbot.analyze_conversation(username))
        elif message.text == 'day report':
            bot.reply_to(message, chatbot.get_daily_report(username, one_hour_before))
        else:
            response = chatbot.chat(str(user_id), message.text)
            bot.reply_to(message, response)

@bot.inline_handler(lambda query: True)
def handle_inline_query(query):
    try:
        query_text = query.query.lower()
        response_text = chatbot.chat(username, query_text) 

        results = [
            telebot.types.InlineQueryResultArticle(
                id='1',
                title='Answer',
                input_message_content=telebot.types.InputTextMessageContent(response_text)
            )
        ]

        bot.answer_inline_query(query.id, results)
    except Exception as e:
        print(e)

bot.infinity_polling()