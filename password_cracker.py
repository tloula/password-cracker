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
import tqdm

from mangle_word import mangle_word

class PasswordCracker():

    def __init__(self):
        self.password_set = set()
        self.username_salt_password_list = []
        self.cracked_set = set()

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
        self.wordlist_file_length = len(lines)
        return lines

    def parse_passwords(self, password_file):
        for password in password_file.readlines():
            self.password_set.add(password.rstrip().split(":")[2])
            self.username_salt_password_list.append(password.rstrip().split(":"))

    def mangle_hash_compare(self, word):
            for mangled_word in mangle_word(word.rstrip()):
                #checked_unsalted = False
                #for usp in self.username_salt_password_list:
                #    if (usp[1] != "" or not checked_unsalted):
                #        if (usp[1] == ""): checked_unsalted = True
                #        salted_mangled_word = mangled_word + usp[1]
                        hash = hashlib.md5(mangled_word.encode())
                        if (hash.hexdigest() in self.password_set):
                            password = mangled_word#.replace(usp[1], "")
                            hashed_password = hash.hexdigest()
                            username = self.get_username(hashed_password)
                            username_password = username + ":" + password
                            if (username_password not in self.cracked_set):
                                #print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, password))
                                return username_password

    def get_username(self, hash):
        for usp in self.username_salt_password_list:
            if (usp[2] == hash): return usp[0]
        return "Error finding user"

    def shut_down(self, wordlist_file, password_file, cracked_file):
        wordlist_file.close()
        password_file.close()
        cracked_file.close()

    def save_cracked_set(self, cracked_file):
        self.cracked_set.remove(None)
        cracked_list = list(self.cracked_set)
        cracked_list.sort()
        for x in cracked_list:
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
                try:
                    pool = Pool(8)
                    self.cracked_set = set(tqdm.tqdm(pool.imap(self.mangle_hash_compare, wordlist), total=self.wordlist_file_length))
                finally:
                    pool.close()
                    pool.join()

                print("\nProcess Complete...")

            finally:
                self.save_cracked_set(cracked_file)
                print(Fore.GREEN + "\nCracked {} passwords".format(len(self.cracked_set)) + Style.RESET_ALL)
                print("\nShutting down...")
                self.shut_down(wordlist_file, password_file, cracked_file)

def main (args):
    cracker = PasswordCracker()
    cracker.run()

if __name__ == "__main__":
        main(sys.argv)
