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
    output += append_numbers(word)

    # Make common letter/symbol or letter/number substitutions
    output += substitute_characters(word)

    # Append common appendages
    output += append_common(word)

    # Advanced mangling
    for x in change_case(word):
        output += substitute_characters(x)

    # Convert to set to remove any duplicates
    return list(set(output))

def change_case(word):
    output = []

    output.append(word.capitalize())
    output.append(word.upper())
    output.append(word.lower())

    for i in range(0, len(word)):
        output.append(word[:i] + word[i].upper() + word[i + 1:])

    return output

def prepend_lowercase_letters(word):
    letters_l = "abcdefghijklmnopqrstuvwxyz"
    return prepend_characters(word, letters_l)

def append_lowercase_letters(word):
    letters_l = "abcdefghijklmnopqrstuvwxyz"
    return append_characters(word, letters_l)

def prepend_uppercase_letters(word):
    letters_u = "ABCDEFGHIJKLMNOPQURSUVWXYZ"
    return prepend_characters(word, letters_u)

def append_uppercase_letters(word):
    letters_u = "ABCDEFGHIJKLMNOPQURSUVWXYZ"
    return append_characters(word, letters_u)

def prepend_symbols(word):
    symbols = "`~!@#$%^&*()_-+=|\}]{[:;?/>.<,"
    return prepend_characters(word, symbols)

def append_symbols(word):
    symbols = "`~!@#$%^&*()_-+=|\}]{[:;?/>.<,"
    return append_characters(word, symbols)

def prepend_numbers(word):
    output = []
    for i in range(0, 100):
        output.append(str(i) + word)
    return output

def append_numbers(word):
    output = []
    for i in range(0, 100):
        output.append(word + str(i))
    return output

def append_characters(word, characters):
    output = []

    for character in characters:
        output.append(word + character)
        for character2 in characters:
            output.append(word + character + character2)

    return output

def prepend_characters(word, characters):
    output = []

    for character in characters:
        output.append(character + word)
        for character2 in characters:
            output.append(character + character2 + word)

    return output

def substitute_characters(word):
    output = []

    substitutions = [
        ("e", "3"),
        ("i", "1"),
        ("i", "|"),
        ("l", "1"),
        ("l", "/"),
        ("l", "\\"),
        ("l", "|"),
        ("s", "5"),
        ("s", "$"),
        ("a", "@"),
        ("o", "0"),
        ("g", "9"),
    ]

    tmp = word
    for orig, sub in substitutions:
        output.append(word.replace(orig, sub))
        tmp = tmp.replace(orig, sub)
        output.append(tmp)

    return output

def append_common(word):
    output = []

    common = [
        "123",
        "1234",
        "12345",
        "123456"
        "0000",
        "00000",
        "000000"
        "321"
        "4321"
        "54321"
        "654321"
        "7654321"
        "87654321"
        "987654321"
    ]

    for x in common:
        output.append(word + x)

    return output
