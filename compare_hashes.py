# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

# Compares a list of hashes to a list of hashed passwords

import datetime as dt
import hashlib
import sys
import time

def get_username(passwords, hash):
    for item in passwords:
        print(item)
        if (item.rstrip().split(":")[2] == hash):
            return item.rstrip().split(":")[0]
    return "Error finding user"

def main (args):

    if len(args) != 3:
        print("Usage: python compare_hashes.py wordlist_hashed.txt passwords.txt")
        exit()

    wordlist_hashed_filename = args[1]
    passwords_filename = args[2]
    cracked_filename = "cracked.txt"

    try:
        wordlist_hashed = open(wordlist_hashed_filename, "r")
        passwords = open(passwords_filename, "r")
        cracked = open(cracked_filename, "a")
    except FileNotFoundError as e:
        print("File not found", e)
        exit()
    else:
        try:
            print("Fetching Passwords...")

            # Save passwords in set
            password_list = []
            username_password_list = []
            for password in passwords.readlines():
                password_list.append(password.rstrip().split(":")[2])
                username_password_list.append(password.rstrip())

            print("Calculating Wordlist Size...")
            lines = wordlist_hashed.readlines()
            total_count = len(lines)

            start = dt.datetime.now()
            current_count = 0

            print("Comparing Hashes...")
            for word in lines:
                current = dt.datetime.now()
                elapsed = current - start
                current_count += 1
                comparisons_sec = int(current_count / (elapsed.seconds + 0.001))
                percent_complete = current_count / total_count
                time_remaining = int((total_count - current_count) / (comparisons_sec + 1))
                print(
                    "Runtime: {} seconds".format(elapsed.seconds),
                    "| Complete: {}".format(current_count),
                    "| Total: {}".format(total_count),
                    "| Comparisons / Second: {}".format(comparisons_sec),
                    "| Percent Complete: {:.2%}".format(percent_complete),
                    "| Estimated Time Remaining: {} seconds".format(time_remaining),
                    end='\r')

                word_parts = word.rstrip().split(":")
                if (word_parts[1] in password_list):
                    password = word_parts[0]
                    hashed_password = word_parts[1]
                    username = get_username(username_password_list, hashed_password)
                    print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, password))
                    cracked.write(username + ":" + password + "\n")

            print("\nProcess Complete...")

        finally:
            print("\nShutting Down...")
            wordlist_hashed.close()
            passwords.close()
            cracked.close()

if __name__ == "__main__":
    main(sys.argv)
