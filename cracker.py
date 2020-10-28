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

    def __init__(self, passwords_filename, wordlist_filename, output_filename, check_salted, output):
        self.password_set = set()
        self.username_salt_password_list = []
        self.cracked_set = set()

        self.wordlist_file_length = 0

        self.check_salted = check_salted
        self.realtime_output = output

        self.passwords_filename = passwords_filename
        self.wordlist_filename = wordlist_filename
        self.output_filename = output_filename

    def open_files(self):
        wordlist_file = open(self.wordlist_filename, "r")
        password_file = open(self.passwords_filename, "r")
        cracked_file = open(self.output_filename, "a")
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
            result = self.hash_compare(mangled_word, "")
            if (result != None): return result
            if (self.check_salted):
                for usp in self.username_salt_password_list:
                    if (usp != ""):
                        result = self.hash_compare(mangled_word, usp[1])
                        if (result != None): return result

    def hash_compare(self, mangled_word, salt):
        hashed_password = hashlib.md5((mangled_word + salt).encode()).hexdigest()
        if (hashed_password in self.password_set):
            username = self.get_username(hashed_password)
            username_password = username + ":" + mangled_word
            if (username_password not in self.cracked_set):
                if(self.realtime_output): print("\nPassword Cracked | Username: {}, Password: {}\n".format(username, mangled_word))
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
                    pool = Pool()
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

    if (len(args) < 3):
        print("Usage: python cracker.py passwords.txt wordlist.txt output.txt -s -o")
        print("-s : Individually check any salted passwords")
        print("-o : Output cracked passwords in real time")
        exit(1)

    check_salted, realtime_output = False, False

    if ("-s" in args): check_salted = True
    if ("-o" in args): realtime_output = True

    cracker = PasswordCracker(args[1], args[2], args[3], check_salted, realtime_output)
    cracker.run()

if __name__ == "__main__":
        main(sys.argv)
