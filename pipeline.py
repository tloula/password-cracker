# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

import datetime as dt
import hashlib
import sys
import time

##### BEGIN WORD MANGLING #####

def mangle_word(word):
    output = []

    # Change Case
    changed_case = change_case(word)
    output += changed_case

    # Prepend and/or append additional lowercase letters
    #prepended_lowercase_letters = prepend_lowercase_letters(word)
    #appended_lowercase_letters = append_lowercase_letters(word)
    #both_lowercase_letters = []
    #for x in prepended_lowercase_letters:
    #    both_lowercase_letters = append_lowercase_letters(x)

    #output += prepended_lowercase_letters
    #output += appended_lowercase_letters
    #output += both_lowercase_letters

    # Prepend and/or append additional uppercase letters
    #prepended_uppercase_letters = prepend_uppercase_letters(word)
    #appended_uppercase_letters = append_uppercase_letters(word)
    #both_lowercase_letters = []
    #for x in prepended_uppercase_letters:
    #    both_uppercase_letters = append_uppercase_letters(x)

    #output += prepended_uppercase_letters
    #output += appended_uppercase_letters
    #output += both_uppercase_letters

    # Prepend and/or append additional symbols
    #prepended_symbols = prepend_symbols(word)
    appended_symbols = append_symbols(word)
    #both_symbols = []
    #for x in prepended_symbols:
    #    both_symbols = append_symbols(x)

    #output += prepended_symbols
    output += appended_symbols
    #output += both_symbols

    # Prepend and/or append additional numbers
    #prepended_numbers = prepend_numbers(word)
    appended_numbers = append_numbers(word)
    #both_numbers = []
    #for x in prepended_numbers:
    #    both_numbers = append_numbers(x)

    #output += prepended_numbers
    output += appended_numbers
    #output += both_numbers

    # Make common letter/symbol or letter/number substitutions
    substituted_characters = substitute_characters(word)
    output += substituted_characters

    ## MANGLE THE MANGLED ##
    for x in changed_case:
    #    output += prepend_lowercase_letters(x)
    #    output += append_lowercase_letters(x)
    #    output += prepend_uppercase_letters(x)
    #    output += append_uppercase_letters(x)
    #    output += prepend_symbols(x)
    #    output += append_symbols(x)
    #    output += prepend_numbers(x)
        output += append_numbers(x)
        output += substitute_characters(x)

    for x in substituted_characters:
        #output += change_case(x)
        #output += prepend_lowercase_letters(x)
        #output += append_lowercase_letters(x)
        #output += prepend_uppercase_letters(x)
        #output += append_uppercase_letters(x)
        #output += prepend_symbols(x)
        #output += append_symbols(x)
        #output += prepend_numbers(x)
        output += append_numbers(x)

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
        ("s", "$"),
        ("s", "5"),
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

##### END WORD MANGLING #####

def get_username(passwords, hash):
    for item in passwords:
        if (item.rstrip().split(":")[2] == hash):
            return item.rstrip().split(":")[0]
    return "Error finding user"

def main (args):

    # Google Collaboratory Path: drive/My Drive/Colab Notebooks/Password Cracker/
    wordlist_filename = "wordlist.txt"
    passwords_filename = "passwords.txt"
    cracked_filename = "cracked_2.txt"

    # Cracked Passwords
    cracked_list = []

    try:
        print("Opening files...")
        wordlist = open(wordlist_filename, "r")
        passwords = open(passwords_filename, "r")
        cracked = open(cracked_filename, "a")
    except FileNotFoundError as e:
        print("File not found", e)
        exit()
    else:
        try:
            print("Parsing wordlist...")
            lines = wordlist.readlines()
            total_count = len(lines)

            print("Parsing unknown password hashes...")
            password_set = set()
            username_password_set = set()
            for password in passwords.readlines():
                password_set.add(password.rstrip().split(":")[2])
                username_password_set.add(password.rstrip())

            start = dt.datetime.now()
            current_count = 0
            comparison_count = 0

            print("Mangling, hashing, and comparing words...")
            for word in lines:
                current = dt.datetime.now()
                elapsed = current - start
                words_sec = current_count / (elapsed.seconds + 0.00000001)
                comparisons_sec = comparison_count / (elapsed.seconds + 0.00000001)
                percent_complete = current_count / total_count
                if (words_sec != 0): time_remaining = int((total_count - current_count) / (words_sec))
                else: time_remaining = 0
                print(
                    "Runtime: {}".format(dt.timedelta(seconds=elapsed.seconds)),
                    "| Total Words: {}".format(total_count),
                    "| Completed Words: {}".format(current_count),
                    "| Words/Sec: {:.2f}".format(words_sec),
                    "| Completed Comparisons: {}".format(comparison_count),
                    "| Comparisons/Sec {:.2f}".format(comparisons_sec),
                    "| Overall: {:.2%}".format(percent_complete),
                    "| ETR: {}".format(dt.timedelta(seconds=time_remaining)),
                    "| Cracked: {}".format(len(cracked_list)),
                    "             ",
                    end='\r')

                mangled_words = mangle_word(word.rstrip())
                for mangled_word in mangled_words:
                    hash = hashlib.md5(mangled_word.encode())
                    if (hash.hexdigest() in password_set):
                        password = mangled_word
                        hashed_password = hash.hexdigest()
                        username = get_username(username_password_set, hashed_password)
                        username_password = username + ":" + password
                        if (username_password not in cracked_list):
                            print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, password))
                            cracked_list.append(username_password)
                    comparison_count += 1

                current_count += 1

            print("\nProcess Complete...")
            print("Cracked {} passwords".format(len(cracked_list)))

        finally:
            print("\nShutting down...")
            cracked_list.sort()
            for x in cracked_list:
                cracked.write(x + "\n")

            wordlist.close()
            passwords.close()
            cracked.close()

if __name__ == "__main__":
    main(sys.argv)
