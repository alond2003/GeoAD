import os


def stats(path=os.getcwd()):
    # print("Debug", path)
    ans = 0
    for filename in os.listdir(path):
        if filename.endswith(".py"):
            with open(os.path.join(path, filename), "r", encoding="utf8") as f:
                file_len = len(f.readlines())
                print(os.path.join(path, filename).replace(os.getcwd(), ""), file_len)
                ans += file_len
        elif (
            os.path.isdir(os.path.join(path, filename))
            and not filename.startswith("__")
            and not filename.startswith(".")
        ):
            ans += stats(os.path.join(path, filename))
    return ans


print(stats())
