import gzip
import os

from parser import Parser

path = os.getcwd() + "/corpus"

articles = ["a", "the", "an"]
pronouns = ["i", "you", "we", "it", "they", "he", "she", "my", "mine", "their", "theirs", "his",
            "her", "that", "this", "us", "me", "him"]
connectives = ["in", "s", "d", "t", "by", "of", "out", "and", "or", "to", "as", "for", "on", "as", "so",
               "also", "though", "but", "not", "may", "who"]
verbs = ["is", "are", "been", "have", "do", "does"]
accents = [",", ".", "-","_", "\\", "~", "/", "{", "}", "[", "]"]


def separate_docs(content):
    return content.split("<doc>")


def read_files():

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".gz"):
                file = gzip.open(os.path.join(root, name), 'rb')
                text = str(file.read())
                text = text.replace("\\r", "").replace("\\n", " ").replace("\\'", "'").replace("\\b", "").lower()
                docs = separate_docs(text)
                for doc in docs:
                    if doc != "b'":
                        parser = Parser()
                        parser.feed(doc)
                        parser.start()
