import logging
import telebot
from telebot import types
import random
import time
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot('6719567455:AAFnnVotReWuMb848dN7A-IlamMjQDU4Fas')

start_time = None
bot_messages = {
    'help': {
        'intro': '\nБот складається з 5 питань, кожне з них має 4 варіанти відповіді. '
                 'Після проходження тесту ви дізнаєтесь результат: кількість відповідей та час проходження.',
        'start_quiz': '\t\nРозпочати опитування: /go'
    },
    'start': {
        'intro': "Ну що, готовий перевірити свої знання?\n"
                 "Тема: Python!\n\n",
        'instructions': "Жми /go якщо продовжуєш або /stop щоб завершити\n"
                        "Щоб отримати більш детальну інформацію натисніть /help"
    },

}
with open('questions.csv', 'r', encoding='utf-8') as csvfile:
    questions_reader = csv.reader(csvfile)
    questions = []
    questions = [row for row in questions_reader]
    #print(questions[1])
    random.shuffle(questions)


good = ["Молодець!", "Чудово!", "Так тримати!", "Ти супер мозок!"]
randomGood = random.choices(good)
random1 = next((x for x in randomGood if x), None)


bad = ["Відповідь не правильна!", "Будь уважніше!", "Спробуй ще!"]
randomBad = random.choices(bad)
random2 =  next((x for x in randomBad if x), None)

@bot.message_handler(commands=['help'])
def handle_help(message):
    logger.info("User requested help")
    intro = bot_messages['help']['intro']
    start_quiz = bot_messages['help']['start_quiz']
    bot.send_message(message.chat.id, f"{intro}{start_quiz}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    logger.info("User started the bot")
    intro = bot_messages['start']['intro']
    instructions = bot_messages['start']['instructions']
    bot.send_message(message.chat.id, f"{intro}{instructions}")

@bot.message_handler(commands=['go'])
def handle_go(message):
    logger.info("User started the quiz")
    points = 0
    start_time = time.time()
    current_question_index = 0
    def send_question():
        nonlocal current_question_index
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        current_question = questions[current_question_index]

        # Iterate over answer options and add them to the markup
        for option in current_question[1:]:
            markup.add(types.KeyboardButton(option))

        bot.send_message(message.chat.id, current_question[0], reply_markup=markup)

    send_question()

    @bot.message_handler(func=lambda message: message.text in questions[current_question_index][1:])
    def handle_answer(message):
        nonlocal points, current_question_index

        user_answer = message.text
        correct_answer = questions[current_question_index][5]

        if user_answer == correct_answer:
            bot.send_message(message.chat.id, random1)
            points += 1
        else:
            bot.send_message(message.chat.id, random2)

        current_question_index += 1
        if current_question_index < len(questions):
            send_question()
        else:
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            bot.send_message(message.chat.id, f'Ви успішно пройшли тест за {time_taken} секунд.')
            bot.send_message(message.chat.id, f'Ви набрали {points} з {len(questions) - 1}.')  # Subtract 1 for the initial question
            logger.info(f"Quiz completed in {time_taken} seconds with {points} points")

bot.polling()



