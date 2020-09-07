from os import listdir

sumy = 0
for i in listdir():
    # print(i)
    if i[-3:] == ".py":
        with open(i, "r", encoding="utf8") as f:
            a = len(f.readlines())
            print(i, a)
            sumy += a


print(sumy)

