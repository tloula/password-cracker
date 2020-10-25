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
    #for i in range(0, len(word)):
    #    newword = word[:i] + word[i].upper() + word[i + 1:]
    #    for j in range(0, 100):
    #        output.append(newword + str(j))
    symbols = "`~!@#$%^&*()_-+=|\}]{[:;?/>.<,"
    letters_u = "ABCDEFGHIJKLMNOPQURSUVWXYZ"
    letters_l = "abcdefghijklmnopqrstuvwxyz"

    for letter in letters_l:
        output.append(word + letter)
        for letter2 in letters_l:
            output.append(word + letter + letter2)
            for letter3 in letters_l:
                output.append(word + letter + letter2 + letter3)
    return output

# Prepend and Append Symbols and Letters