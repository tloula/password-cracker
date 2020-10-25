# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

from colorama import Fore, Style

import datetime as dt
import hashlib
import sys
import time

from mangle_word import mangle_word

def get_username(passwords, hash):
    for usp in passwords:
        if (usp[2] == hash): return usp[0]
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
            username_salt_password = []
            for password in passwords.readlines():
                password_set.add(password.rstrip().split(":")[2])
                username_salt_password.append(password.rstrip().split(":"))

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

                for mangled_word in mangle_word(word.rstrip()):
                    checked_unsalted = False
                    for usp in username_salt_password:
                        if (usp[1] != "" or not checked_unsalted):
                            if (usp[1] == ""): checked_unsalted = True
                            salted_mangled_word = mangled_word + usp[1]
                            hash = hashlib.md5(salted_mangled_word.encode())
                            if (hash.hexdigest() in password_set):
                                password = salted_mangled_word.replace(usp[1], "")
                                hashed_password = hash.hexdigest()
                                username = get_username(username_salt_password, hashed_password)
                                username_password = username + ":" + password
                                if (username_password not in cracked_list):
                                    print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, password))
                                    cracked_list.append(username_password)
                            comparison_count += 1

                current_count += 1

            print("\nProcess Complete...")
            print(Fore.GREEN + "\nCracked {} passwords".format(len(cracked_list)) + Style.RESET_ALL)

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