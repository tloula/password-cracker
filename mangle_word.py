def mangle_word(word):
    output = []
    #word = word.replace("e", "3")
    #word = word.replace("i", "1")
    #word = word.replace("s", "$")
    #word = word.replace("a", "@")
    #word = word.replace("o", "0")
    #word = word.replace("g", "9")
    #for i in range(0, 100):
    #    output.append(word + str(i))
    for i in range(0, len(word)):
        newword = word[:i] + word[i].upper() + word[i + 1:]
        output.append(newword)
    return output
