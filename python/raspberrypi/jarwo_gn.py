import sys
import asyncio
import random

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

RANDOM=random.randint(0,99)
GUESSTRY=0
GAMEON=False
# Enable logging
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def newRandom():
	global RANDOM
	RANDOM=random.randint(0,99)
	# print(f'RANDOM: {RANDOM}')

def ahint(answer, guess):
	print(f'guess: {guess} answer: {answer}')
	global GUESSTRY
	# GUESSTRY+=1
	if answer > guess:
		return (f'[{GUESSTRY}] kekecilan')
	else:
		return  (f'[{GUESSTRY}] ketinggian')

async def startGame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	global GAMEON
	if GAMEON is False:

		"""Send a message when the command /help is issued."""
		newRandom()

		await update.message.reply_text("aku punya angka 1-99.\nCoba tebak dalam 6 kali percobaan...")
	else:
		await update.message.reply_text("permainan sedang berjalan\nSilahkan teruskan...")

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""Send a message when the command /start is issued."""
	user = update.effective_user
	await update.message.reply_html(
		rf"Hi {user.mention_html()}!",
		reply_markup=ForceReply(selective=True),
	)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""Send a message when the command /help is issued."""
	await update.message.reply_text("Help!")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
# 	"""Echo the user message."""
# 	await update.message.reply_text(update.message.text)

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	global RANDOM
	global GUESSTRY
	global GAMEON
	"""Echo the user message."""
	# guess=update.message.text
	# if content_type != 'text':
	# 	# await self.sender.sendMessage('Give me a number, please.')
	# 	await update.message.reply_text('harus angka!')
	# 	return

	try:
		# guess = int(msg['text'])
		guess=int(update.message.text)
	except ValueError:
		# await self.sender.sendMessage('Give me a number, please.')
		await update.message.reply_text('harus angka!')
		return

	# check the guess against the answer ...
	# print(f'guess: {guess} RANDOM: {RANDOM}')
	if guess != RANDOM:
		# give a descriptive hint
		GUESSTRY+=1
		if GUESSTRY> 6:
			GAMEON=False
			await update.message.reply_text(f'percobaan gagal melebihi kuota!\kamu kalah\njawaban yang benar adalah: {RANDOM}')
			GUESSTRY=0
			return
		else:
			hint = ahint(RANDOM, guess)
			await update.message.reply_text(hint)
	else:
		await update.message.reply_text(f'benarrr!\nKamu berhasil menebak dalam {GUESSTRY+1} percobaan\n/tebak jika ingin mulai lagi')
		GUESSTRY=0
		GAMEON=False
		# self.close()
	# await update.message.reply_text(update.message.text)

def main() -> None:
	"""Start the bot."""
	# Create the Application and pass it your bot's token.
	application = Application.builder().token('64:rKe0').build()

	# on different commands - answer in Telegram
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("tebak", startGame))
	application.add_handler(CommandHandler("help", help_command))

	# on non command i.e message - echo the message on Telegram
	# application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))

	# Run the bot until the user presses Ctrl-C
	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()



# import telepot
# from telepot.aio.loop import MessageLoop
# from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
#
# """
# $ python3.5 guessa.py <token>
#
# Guess a number:
#
# 1. Send the bot anything to start a game.
# 2. The bot randomly picks an integer between 0-99.
# 3. You make a guess.
# 4. The bot tells you to go higher or lower.
# 5. Repeat step 3 and 4, until guess is correct.
# """
#
# class Player(telepot.aio.helper.ChatHandler):
# 	def __init__(self, *args, **kwargs):
# 		super(Player, self).__init__(*args, **kwargs)
# 		self._answer = random.randint(0,99)
#
# 	def _hint(self, answer, guess):
# 		if answer > guess:
# 			return 'ketinggian'
# 		else:
# 			return 'kekecilan'
#
# 	async def open(self, initial_msg, seed):
# 		await self.sender.sendMessage('Guess my number')
# 		return True  # prevent on_message() from being called on the initial message
#
# 	async def on_chat_message(self, msg):
# 		content_type, chat_type, chat_id = telepot.glance(msg)
#
# 		if content_type != 'text':
# 			await self.sender.sendMessage('Give me a number, please.')
# 			return
#
# 		try:
# 		guess = int(msg['text'])
# 		except ValueError:
# 			await self.sender.sendMessage('Give me a number, please.')
# 			return
#
# 		# check the guess against the answer ...
# 		if guess != self._answer:
# 			# give a descriptive hint
# 			hint = self._hint(self._answer, guess)
# 			await self.sender.sendMessage(hint)
# 		else:
# 			await self.sender.sendMessage('Correct!')
# 			self.close()
#
# 	async def on__idle(self, event):
# 		await self.sender.sendMessage('Game expired. The answer is %d' % self._answer)
# 		self.close()
#
#
# TOKEN = '5592035909:AAEEQkDoWUwlOfxWJautVreSMZUXs7O9uyg'
#
# bot = telepot.aio.DelegatorBot(TOKEN, [
# 	pave_event_space()(
# 		per_chat_id(), create_open, Player, timeout=10),
# ])
#
# loop = asyncio.get_event_loop()
# loop.create_task(MessageLoop(bot).run_forever())
# print('Listening ...')
#
# loop.run_forever()
