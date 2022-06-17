import random

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
text = input()

correct = 0
wrong = 0

while text != "Закончить":
    i = random.randint(0, len(bd) - 1)
    correctForm = correctWords[i]
    usedCorrect.append(correctForm)
    del correctWords[i]
    word = bd[i]
    used.append(bd[i])
    del bd[i]
    print(word.lower())
    text = input()
    if text != word:
        wrong += 1
        print("Неверно, правильно вот так:", word)
        print(correctForm.rstrip())
    else:
        correct += 1
        print("Верно!")
    print()
    if len(bd) == 0:
        print("Ваш счёт:")
        print("Верно поставленных ударений:", correct)
        print("Неверно поставленных ударений:", wrong)
        bd = used[:]
        used = []
        correctWords = usedCorrect[:]
        usedCorrect = []
        print()
