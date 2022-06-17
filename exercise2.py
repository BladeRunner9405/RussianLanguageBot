import random


def getRandomWord():
    global bd, used, usedCorrect, correctWords
    i = random.randint(0, len(bd) - 1)
    correctForm = correctWords[i]
    usedCorrect.append(correctForm)
    del correctWords[i]
    word = bd[i]
    used.append(bd[i])
    del bd[i]
    return word, correctForm


def check(text, word, correctForm):
    global correct, wrong
    if text != word:
        wrong += 1
        return f"Неверно, правильно вот так: {word}\n{correctForm.rstrip()}\n"
    else:
        correct += 1
        return "Верно!\n"


def wordsOver():
    global used, usedCorrect, bd, correctWords
    bd = used[:]
    used = []
    correctWords = usedCorrect[:]
    usedCorrect = []
    return f'Ваш счёт:\nВерно поставленных ударений: {correct}\nНеверно поставленных ударений {wrong}\n'


def getMessage():
    return input()


bd = []
correctWords = []
usedCorrect = []

with open("accentTest.txt", "r", encoding="UTF-8") as file:
    for elem in file:
        string = elem.split()
        if not string[0][0].isdigit():
            correctWords.append(elem)
            if string[0][-1] == ',':
                string[0] = string[0][:-1]
            bd.append(string[0])

used = []
print("Введите что-нибудь для начала")
text = getMessage()

correct = 0
wrong = 0

while text != "Закончить":
    word, correctForm = getRandomWord()
    print(word.lower())
    text = getMessage()
    print(check(text, word, correctForm))
    if len(bd) == 0:
        wordsOver()
