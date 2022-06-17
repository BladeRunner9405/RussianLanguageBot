# Импортируем необходимые классы.
import os
import sqlite3
import random

from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, Filters

# Запускаем логгирование
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
# )
#
# logger = logging.getLogger(__name__)

TOKEN = '5444648065:AAFCzEZzrIO5ZLd8NYbQup2SRcofO1JLd_M'

base_reply_keyboard = [['/start', '/help'],
                       ['2', '7']]
base_markup = ReplyKeyboardMarkup(base_reply_keyboard, one_time_keyboard=True)


# reply_keyboard = [['/address', '/phone'],
#                   ['/site', '/work_time']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.

class Db:
    def add_user(self, id, username, first_name, last_name):
        database = 'Users.db'
        con = sqlite3.connect(database)
        cur = con.cursor()
        if (id,) not in cur.execute(f'SELECT id FROM users').fetchall():
            cur.execute('INSERT INTO users VALUES (?,?,?,?)',
                        tuple([id, username, first_name, last_name])).fetchall()
            con.commit()

    def get_all(self):
        database = 'Users.db'
        con = sqlite3.connect(database)
        cur = con.cursor()
        answer = cur.execute(f'SELECT id, username, first_name, last_name FROM users').fetchall()
        result = []
        for elem in answer:
            id, username, first_name, last_name = elem
            result.append([id, username, first_name, last_name])
        return result


class User:
    def __init__(self, id):
        self.id = id
        self.exNum = 0
        self.started = False
        self.exercise = None

    def getAll(self):
        return self.exNum, self.started, self.exercise

    def newExNum(self, num):
        self.exNum = num

    def setStarted(self, a):
        self.started = a

    def setExercise(self, exercise):
        self.exercise = exercise

    def getExercise(self):
        return self.exercise


database = Db()
Users = {}


class AllExercise:
    class exercise2:
        AllWords = []
        AllCorrectForms = []

        words = []
        correctForms = []

        wrongWords = []
        wrongWordsCorrectForms = []

        count = 0
        correct = 0
        wrong = 0
        word = ''
        correctForm = ''

        answered = True

        def __init__(self, update):
            self.update = update

        def start(self, update):
            reply_keyboard = [['Начать сначала', 'по неправильным'], ['Хватит']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'Задание 2. Ударения', reply_markup=markup)

            self.AllWords = []
            self.AllCorrectForms = []

            with open("accentTest.txt", "r", encoding="UTF-8") as file:
                for elem in file:
                    string = elem.split()
                    if not string[0][0].isdigit():
                        self.AllCorrectForms.append(elem)
                        if string[0][-1] == ',':
                            string[0] = string[0][:-1]
                        self.AllWords.append(string[0])
            self.words = self.AllWords[:]
            self.correctForms = self.AllCorrectForms[:]
            self.count = len(self.words)
            self.wrongWords = []
            self.wrongWordsCorrectForms = []

            self.correct = 0
            self.wrong = 0

        def stop(self, update):
            statics = self.getStatics()
            self.end()
            update.message.reply_text(statics, reply_markup=base_markup)

        def getRandomWord(self):
            if self.answered:
                i = random.randint(0, len(self.words) - 1)
                correctForm = self.correctForms[i]
                del self.correctForms[i]
                word = self.words[i]
                del self.words[i]
                self.answered = False
                return word, correctForm
            else:
                return self.word, self.correctForm

        def check(self, text, word, correctForm):
            if text.lower() != word.lower():
                return f"Вы ошиблись в написании слова!"
            elif text[1:] != word[1:]:
                self.answered = True
                self.wrong += 1
                self.wrongWords.append(word)
                self.wrongWordsCorrectForms.append(correctForm)
                return f"Неверно, правильно вот так: {word}\n{correctForm.rstrip()}\n"
            else:
                self.answered = True
                self.correct += 1
                return "Верно!\n"

        def byMistakes(self):
            self.wrong = 0
            self.correct = 0
            self.words = self.wrongWords[:]
            self.correctForms = self.wrongWordsCorrectForms[:]
            self.wrongWords = []
            self.wrongWordsCorrectForms = []
            self.count = len(self.words)

        def end(self):
            self.wrong = 0
            self.correct = 0
            self.words = self.AllWords[:]
            self.correctForms = self.AllCorrectForms[:]
            self.wrongWords = []
            self.wrongWordsCorrectForms = []
            self.count = len(self.words)

        def getStatics(self):
            wrong = self.wrong
            correct = self.correct
            return f'Ваш счёт:\nВерно поставленных ударений: {correct}\nНеверно поставленных ударений {wrong}\n'

        def getMessage(self, update):
            text = update.message.text
            return text

        def getQuestion(self, update):
            if len(self.words) != 0:
                self.word, self.correctForm = self.getRandomWord()
                # message = f'{self.correct + self.wrong + 1}/{self.count}:\n{self.word.lower()}'
                update.message.reply_text(self.word.lower())

        def getAnswer(self, update):
            text = self.getMessage(update)
            if text.lower() == "по неправильным":

                self.answered = True

                reply_keyboard = [['Начать сначала'], ['Хватит']]
                if self.wrong != 0:
                    reply_keyboard[0].append('по неправильным')
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                update.message.reply_text(self.getStatics(), reply_markup=markup)
                self.byMistakes()

            elif text.lower() == "начать сначала":
                self.answered = True

                reply_keyboard = [['Начать сначала', 'по неправильным'], ['Хватит']]

                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                update.message.reply_text(self.getStatics(), reply_markup=markup)
                self.end()
            else:

                update.message.reply_text(self.check(text, self.word, self.correctForm))
                if len(self.words) == 0 and self.answered:
                    update.message.reply_text('Cлова кончились!')
                    reply_keyboard = [['Начать сначала'], ['Хватит']]
                    if self.wrong != 0:
                        reply_keyboard[0].append('по неправильным')
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                        update.message.reply_text('Вы можете начать сначала или пройтись по неправильным!',
                                                  reply_markup=markup)
                    else:
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                        update.message.reply_text('Все слова правильные! Начать сначала?', reply_markup=markup)
                    update.message.reply_text(self.getStatics(), reply_markup=markup)

    class exercise7:
        AllWords = []
        AllCorrectForms = []

        words = []
        correctForms = []

        wrongWords = []
        wrongWordsCorrectForms = []

        count = 0
        correct = 0
        wrong = 0
        word = ''
        correctForm = ''

        answered = True

        def __init__(self, update):
            self.update = update

        def start(self, update):
            self.AllWords = []
            self.AllCorrectForms = []

            reply_keyboard = [['Начать сначала', 'по неправильным'], ['Хватит']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'Задание 7. Паронимы', reply_markup=markup)
            with open("paronymsTest.txt", "r", encoding="UTF-8") as file:
                for elem in file:
                    string = elem.split(' – ')
                    if len(string) == 2:
                        self.AllCorrectForms.append(string[1].rstrip().lower())
                        self.AllWords.append(string[0].lower())
            self.words = self.AllWords[:]
            self.correctForms = self.AllCorrectForms[:]
            self.count = len(self.words)
            self.wrongWords = []
            self.wrongWordsCorrectForms = []

            self.correct = 0
            self.wrong = 0

        def stop(self, update):
            statics = self.getStatics()
            self.end()
            update.message.reply_text(statics, reply_markup=base_markup)

        def getRandomWord(self):
            if self.answered:
                i = random.randint(0, len(self.words) - 1)
                correctForm = self.correctForms[i]
                del self.correctForms[i]
                word = self.words[i]
                del self.words[i]
                self.answered = False
                return word, correctForm
            else:
                return self.word, self.correctForm

        def check(self, text, word, correctForm):
            if text.lower() != correctForm.lower():
                self.answered = True
                self.wrong += 1
                self.wrongWords.append(word)
                self.wrongWordsCorrectForms.append(correctForm)
                return f"Неверно, правильно вот так:\n{word} - {correctForm}"
            else:
                self.answered = True
                self.correct += 1
                return "Верно!\n"

        def byMistakes(self):
            self.wrong = 0
            self.correct = 0
            self.words = self.wrongWords[:]
            self.correctForms = self.wrongWordsCorrectForms[:]
            self.wrongWords = []
            self.wrongWordsCorrectForms = []
            self.count = len(self.words)

        def end(self):
            self.wrong = 0
            self.correct = 0
            self.words = self.AllWords[:]
            self.correctForms = self.AllCorrectForms[:]
            self.wrongWords = []
            self.wrongWordsCorrectForms = []
            self.count = len(self.words)

        def getStatics(self):
            wrong = self.wrong
            correct = self.correct
            return f'Ваш счёт:\nВерно подставленных паронимов: {correct}\nНеверно подставленных паронимов {wrong}\n'

        def getMessage(self, update):
            text = update.message.text
            return text

        def getQuestion(self, update):
            if len(self.words) != 0:
                word_correctForm = self.getRandomWord()
                a = random.randint(0, 1)
                self.word = word_correctForm[a]
                self.correctForm = word_correctForm[1 - a]
                # message = f'{self.correct + self.wrong + 1}/{self.count}:\n{self.word.lower()}'
                update.message.reply_text(self.word.lower())

        def getAnswer(self, update):
            text = self.getMessage(update)
            if text.lower() == "по неправильным":

                self.answered = True

                reply_keyboard = [['Начать сначала'], ['Хватит']]
                if self.wrong != 0:
                    reply_keyboard[0].append('по неправильным')
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                update.message.reply_text(self.getStatics(), reply_markup=markup)
                self.byMistakes()

            elif text.lower() == "начать сначала":
                self.answered = True

                reply_keyboard = [['Начать сначала', 'по неправильным'], ['Хватит']]

                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                update.message.reply_text(self.getStatics(), reply_markup=markup)
                self.end()
            else:

                update.message.reply_text(self.check(text, self.word, self.correctForm))
                if len(self.words) == 0:
                    update.message.reply_text('Cлова кончились!')
                    reply_keyboard = [['Начать сначала'], ['Хватит']]
                    if self.wrong != 0:
                        reply_keyboard[0].append('по неправильным')
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                        update.message.reply_text('Вы можете начать сначала или пройтись по неправильным!',
                                                  reply_markup=markup)
                    else:
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                        update.message.reply_text('Все слова правильные! Начать сначала?', reply_markup=markup)
                    update.message.reply_text(self.getStatics(), reply_markup=markup)

    def getExercise(self, num):
        if num == 2:
            return self.exercise2
        if num == 7:
            return self.exercise7
        return None


def error(update, context):
    update.message.reply_text(f'Ошибка: {update.message.text}\n')


# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update, context):
    message = f"Привет {update.message.from_user['first_name']}! Краткое описание\n\n "
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    id = update.message.from_user['id']
    if not first_name:
        first_name = 'Пользователь'
    if not last_name:
        last_name = 'None'
    if not username:
        username = 'None'

    database.add_user(id, username, first_name, last_name)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    return help(update, context)


def help(update, context):
    message = f"Описание"
    update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=base_markup)


def redirection(update, context):
    id = update.message.from_user['id']

    if id not in Users:
        Users[id] = User(id)
        Users[id].setStarted(False)
        Users[id].setExercise(None)
    if not Users[id].getExercise():
        if update.message.text.isdigit():
            Users[id].newExNum(int(update.message.text))
            exNum = int(update.message.text)
            exercise = AllExercise().getExercise(exNum)
            if exercise:
                user_exercise = exercise(update)
                user_exercise.start(update)
                user_exercise.getQuestion(update)
                Users[id].setExercise(user_exercise)
                Users[id].setStarted(True)
                user_exercise = None
            else:
                Users[id].newExNum(0)
                update.message.reply_text("Этого задания пока что в боте нету", parse_mode=ParseMode.HTML,
                                          reply_markup=base_markup)

        else:
            help(update, context)
    else:
        if update.message.text == "Хватит":
            Users[id].getExercise().stop(update)
            Users[id].newExNum(0)
            Users[id].setExercise(None)
            Users[id].setStarted(False)
        else:

            Users[id].getExercise().getAnswer(update)
            Users[id].getExercise().getQuestion(update)


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.

    text_handler = MessageHandler(Filters.text, redirection)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', 5000)),
                          url_path='5444648065:AAFCzEZzrIO5ZLd8NYbQup2SRcofO1JLd_M',
                          webhook_url=+ '5444648065:AAFCzEZzrIO5ZLd8NYbQup2SRcofO1JLd_M'
                          )

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
main()
