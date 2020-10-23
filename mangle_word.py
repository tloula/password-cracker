def mangle_word(word):
    output = []
    #for i in range(0, 1000):
    #    output.append(str(i) + word)
    word = word.replace("e", "3")
    word = word.replace("i", "!")
    word = word.replace("s", "$")
    word = word.replace("a", "@")
    word = word.replace("o", "0")
    word = word.replace("g", "9")
    return [word]
