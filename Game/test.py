def ReadResults():
    with open("res.txt", "r+") as file:
        x = file.readlines(6)
        print(x)
        for line in x[:6]:
            print(line)

x = "1;123\n2;34\n3;344\n"
ReadResults()