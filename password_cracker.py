# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

from colorama import Fore, Style
from multiprocessing import Pool

import datetime as dt
import hashlib
import sys
import time

from mangle_word import mangle_word

class PasswordCracker():

    def __init__(self):
        self.password_set = set()
        self.username_salt_password_list = []
        self.cracked_list = []

        # Progress Data
        self.wordlist_file_length = 0
        self.start_time = 0
        self.current_count = 0
        self.comparison_count = 0

    def open_files(self):
        # Google Collaboratory Path: drive/My Drive/Colab Notebooks/Password Cracker/
        wordlist_file = open("wordlist.txt", "r")
        password_file = open("passwords.txt", "r")
        cracked_file = open("cracked_new.txt", "a")
        return wordlist_file, password_file, cracked_file

    def parse_wordlist(self, wordlist_file):
        lines = wordlist_file.readlines()
        self.wordlist_length = len(lines)
        return lines

    def parse_passwords(self, password_file):
        for password in password_file.readlines():
            self.password_set.add(password.rstrip().split(":")[2])
            self.username_salt_password_list.append(password.rstrip().split(":"))

    def mangle_hash_compare(self, word):
            self.update_progress()
            mangled_words = mangle_word(word.rstrip())
            for mangled_word in mangled_words:
                self.hash_compare(mangled_word)

            self.current_count += 1

    def hash_compare(self, mangled_word):
        checked_unsalted = False
        for usp in self.username_salt_password_list:
            if (usp[1] != "" or not checked_unsalted):
                if (usp[1] == ""): checked_unsalted = True
                salted_mangled_word = mangled_word + usp[1]
                hash = hashlib.md5(salted_mangled_word.encode())
                if (hash.hexdigest() in self.password_set):
                    self.cracked_password(hash, salted_mangled_word, usp[1])
                self.comparison_count += 1

    def cracked_password(self, hash, salted_mangled_word, salt):
        password = salted_mangled_word.replace(salt, "")
        hashed_password = hash.hexdigest()
        username = self.get_username(hashed_password)
        username_password = username + ":" + password
        if (username_password not in self.cracked_list):
            print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, password))
            self.cracked_list.append(username_password)

    def update_progress(self):
        current = dt.datetime.now()
        elapsed = current - self.start_time
        words_sec = self.current_count / (elapsed.seconds + 0.00000001)
        comparisons_sec = self.comparison_count / (elapsed.seconds + 0.00000001)
        percent_complete = self.current_count / self.wordlist_length
        if (words_sec != 0): time_remaining = int((self.wordlist_length - self.current_count) / (words_sec))
        else: time_remaining = 0
        print(
            "Runtime: {}".format(dt.timedelta(seconds=elapsed.seconds)),
            "| Total Words: {}".format(self.wordlist_length),
            "| Completed Words: {}".format(self.current_count),
            "| Words/Sec: {:.2f}".format(words_sec),
            "| Completed Comparisons: {}".format(self.comparison_count),
            "| Comparisons/Sec {:.2f}".format(comparisons_sec),
            "| Overall: {:.2%}".format(percent_complete),
            "| ETR: {}".format(dt.timedelta(seconds=time_remaining)),
            "| Cracked: {}".format(len(self.cracked_list)),
            "             ",
            end='\r')

    def get_username(self, hash):
        for usp in self.username_salt_password_list:
            if (usp[2] == hash): return usp[0]
        return "Error finding user"

    def shut_down(self, wordlist_file, password_file, cracked_file):
        self.save_cracked_list(cracked_file)
        wordlist_file.close()
        password_file.close()
        cracked_file.close()

    def save_cracked_list(self, cracked_file):
        self.cracked_list.sort()
        for x in self.cracked_list:
            cracked_file.write(x + "\n")

    def run(self):
        try:
            print("Opening files...")
            wordlist_file, password_file, cracked_file = self.open_files()
        except FileNotFoundError as e:
            print("File not found", e)
            exit()
        else:
            try:
                print("Parsing wordlist...")
                wordlist = self.parse_wordlist(wordlist_file)

                print("Parsing unknown password hashes...")
                self.parse_passwords(password_file)

                self.start_time = dt.datetime.now()
                print("Mangling, hashing, and comparing words...")
                #for word in wordlist:
                #    self.mangle_hash_compare(word)

                try:
                    pool = Pool(4)                                  # Create a multiprocessing Pool
                    pool.map(self.mangle_hash_compare, wordlist)    # process wordlist iterable with pool
                finally:
                    pool.close()
                    pool.join()

                print("\nProcess Complete...")
                print(Fore.GREEN + "\nCracked {} passwords".format(len(self.cracked_list)) + Style.RESET_ALL)

            finally:
                print("\nShutting down...")
                self.shut_down(wordlist_file, password_file, cracked_file)

def main (args):
    cracker = PasswordCracker()
    cracker.run()

if __name__ == "__main__":
        main(sys.argv)
