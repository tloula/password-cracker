import re
import sys

def main(args):

    source_filename = "bible.txt"
    destination_filename = "wordlist.txt"

    with open(source_filename) as source, open(destination_filename, 'a') as destination:
      destination.write('\n'.join(set(re.findall("[a-zA-Z]+", source.read()))))

    print("wordlist complete")

if __name__ == "__main__":
    main(sys.argv)
