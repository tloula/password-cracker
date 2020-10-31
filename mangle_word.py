# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

def mangle_word(word):
    output = []

    # Change Case
    output += change_case(word)

    # Prepend and/or append additional lowercase letters
    output += append_lowercase_letters(word)

    # Prepend and/or append additional uppercase letters
    output += append_uppercase_letters(word)

    # Prepend and/or append additional symbols
    output += append_symbols(word)

    # Prepend and/or append additional numbers
    output += append_numbers(word, False, 100)

    # Make common letter/symbol or letter/number substitutions
    output += substitute_characters(word)

    # Append common appendages
    output += append_common(word)

    # Advanced mangling
    for x in append_symbols(word, True):
        output += append_symbols(x)

    for x in append_numbers(word):
        output += append_symbols(x)

    # Dates
    #for y in range(1950, 2020):
    #    for m in range(13):
    #        for d in range(32):
    #            output.append(word + str(m) + str(d) + str(y))
    #            output.append(str(m) + str(d) + str(y) + word)
    output.append(word + str(12311999))
    output.append(str(1980) + word)

    # Convert to set to remove any duplicates
    return list(set(output))

def change_case(word):
    output = [word]

    output.append(word.upper())
    output.append(word.lower())

    # Capitalize one letter in a lowercase word at a time
    for i in range(len(word)):
        nw = word.lower()
        output.append(nw[:i] + nw[i].upper() + nw[i + 1:])

    # Capitalize one letter in an uppercase word at a time
    for i in range(len(word)):
        nw = word.upper()
        output.append(nw[:i] + nw[i].lower() + nw[i + 1:])

    return list(set(output))

def append_lowercase_letters(word, front=False):
    letters_l = "abcdefghijklmnopqrstuvwxyz"
    return append_characters(word, letters_l, front)

def append_uppercase_letters(word, front=False):
    letters_u = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return append_characters(word, letters_u, front)

def append_symbols(word, front=False):
    symbols = "!@#$%^&*()-=_+<>?"
    return append_characters(word, symbols, front)

def append_numbers(word, front=False, n=10):
    output = [word]
    if (front):
        for i in range(n):
            output.append(str(i) + word)
    else:
        for i in range(n):
            output.append(word + str(i))
    return output

def append_characters(word, characters, front=False):
    output = [word]
    if (front):
        for character in characters:
            output.append(character + word)
    else:
        for character in characters:
            output.append(word + character)
    return output

def substitute_characters(word):
    output = [word]

    substitutions = [
        #("a", "^"),
        #("b", "8"),
        #("c", "<"),
        #("c", "("),
        #("c", "["),
        #("c", "{"),
        #("d", "|)"),
        #("d", "|>"),
        ("e", "3"),
        ("i", "1"),
        #("I", "1"),
        #("i", ":"),
        #("i", ";"),
        #("i", "|"),
        #("l", "1"),
        #("l", "/"),
        #("l", "\\"),
        #("l", "|"),
        ("s", "5"),
        ("s", "$"),
        ("s", "z"),
        ("a", "@"),
        ("o", "0"),
        #("g", "9"),
        #("y", "?"),
    ]

    tmp = word
    for orig, sub in substitutions:
        output.append(word.replace(orig, sub))
        tmp = tmp.replace(orig, sub)
        output.append(tmp)

    return list(set(output))

def append_common(word, front=False):
    output = [word]

    common = [
        "123",
        "1234",
        "12345",
        "123456"
        "0000",
        "00000",
        "000000",
        "321",
        "4321",
        "54321",
        "654321",
        "7654321",
        "87654321",
        "987654321",
    ]

    if (front):
        for x in common:
            output.append(x + word)
    else:
        for x in common:
            output.append(word + x)

    return output
