from os import listdir

for i in listdir():
    # print(i)
    if i[-3:] == ".py":
        with open(i, "r") as f:
            print(i, len(f.readlines()))

