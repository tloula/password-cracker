# ********************************************* #
# MD5 Password Hash Cracker                     #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

# Generates a list of hashes given a wordlist

import datetime as dt
import hashlib
import sys
import time

from mangle_word import mangle_word

def main (args):

    if len(args) != 2:
        print("Usage: python generate_hashes.py wordlist.txt")
        exit()

    wordlist_filename = args[1]
    index = wordlist_filename.find('.')
    hashes_filename = wordlist_filename[:index] + '_hashed' + wordlist_filename[index:]

    try:
        open(hashes_filename, 'w').close()
        wordlist = open(wordlist_filename, "r")
        hashes = open(hashes_filename, "a")
    except FileNotFoundError as e:
        print("File not found", e)
        exit()
    else:
        try:
            print("Fetching wordlist...")
            lines = wordlist.readlines()
            total_count = len(lines)

            start = dt.datetime.now()
            current_count = 0

            print("Generating mangled & hashed wordlist...")
            for word in lines:
                current = dt.datetime.now()
                elapsed = current - start
                current_count += 1
                words_sec = int(current_count / (elapsed.seconds + 0.001))
                percent_complete = current_count / total_count
                time_remaining = int((total_count - current_count) / (words_sec + 1))
                print(
                    "Runtime: {} seconds".format(elapsed.seconds),
                    "| Complete: {}".format(current_count),
                    "| Total: {}".format(total_count),
                    "| Mangled Hash Sets / Second: {}".format(words_sec),
                    "| Percent Complete: {:.2%}".format(percent_complete),
                    "| Estimated Time Remaining: {} seconds".format(time_remaining),
                    end='\r')

                mangled_words = mangle_word(word.rstrip())
                for mangled_word in mangled_words:
                    hash = hashlib.md5(mangled_word.encode())
                    hashes.write(mangled_word + ":" + hash.hexdigest() + '\n')

            print("\nWordlist Complete...")

        finally:
            print("\nShutting down...")
            wordlist.close()
            hashes.close()

if __name__ == "__main__":
    main(sys.argv)
