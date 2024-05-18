import os.path


def writeResult( sScore, sName):

    incert = False
    x = []
    if os.path.exists('res.txt'):
        with open("res.txt", "r") as file:
            x = file.readlines()

    with open("res.txt", "w") as file:
        for i in range(0, 5):
            try:
                if not incert:
                    score, name = x[i].split(";")
                    if sScore > int(score):
                        incert = True
                        file.write(str(sScore) + ";" + str(sName) + "\n")
                    else:
                        file.write(score + ";" + name)
                else:
                    file.write(x[i - 1])
            except IndexError:
                file.write(str(sScore) + ";" + str(sName) + "\n")
                break


def readResults():
    with open("res.txt", "r+") as file:
        x = file.readlines()
    return x


for i in range(3):
    for l in ['a', 'b', 'c']:
        writeResult(i, l)

for el in readResults():
    print(el)
