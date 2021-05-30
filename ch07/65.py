def main():
    from os import path
    import json

    fp = "64/questions-words.txt"
    s = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), "64/data.json"), "r"))
    count_semantic = 0
    accuracy_semantic = 0
    count_syntactic = 0
    accuracy_syntactic = 0
    semantic = True
    for t in s:
        if t[0:6] == ": gram":
            semantic = False
        elif t[0] == ":":
            semantic = True
        else:
            if semantic:
                count_semantic += 1
                if t[3] == t[4]:
                    accuracy_semantic += 1
            else:
                count_syntactic += 1
                if t[3] == t[4]:
                    accuracy_syntactic += 1

    print(f"accuracy semantic: {accuracy_semantic / count_semantic}")
    print(f"accuracy syntactic: {accuracy_syntactic / count_syntactic}")


if __name__ == "__main__":
    main()
