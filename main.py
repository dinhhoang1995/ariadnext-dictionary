import json

from typing import List


class Dictionary:
    """
    Class Dictionary
    """

    def __init__(self):
        self.root = {}

    def get_dictionary(self):
        """
        Get dictionary dict presentation
        :return:
        """
        return self.root

    def insert_words(self, *words):
        """
        Insert multi words to the dictionary
        :param words:
        :return:
        """
        for word in words:
            self.insert(word)

    def insert(self, word):
        """
        Insert a word to the dictionary
        :param word:
        :return:
        """
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node.setdefault("_end", "_end")

    def search(self, word) -> bool:
        """
        Search a word in the dictionary
        :param word:
        :return: True if the word is in the dictionary else False
        """
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        if "_end" in node:
            return True
        return False

    def _walk_dictionary(self, node, prefix, words):
        if "_end" not in node or ("_end" in node and len(node) > 1):
            children = [child for child in node if child != "_end"]
            for char in children:
                word = prefix + char
                if "_end" in node[char]:
                    words.append(word)
                self._walk_dictionary(node[char], word, words)

    def list_words_starting_with_prefix(self, prefix) -> List[str]:
        """
        List all words in the dictionary starting with the prefix
        :param prefix:
        :return: List of words
        """
        node = self.root
        words = []
        for char in prefix:
            if char not in node:
                return words
            node = node[char]

        if "_end" in node:
            words.append(prefix)

        self._walk_dictionary(node, prefix, words)
        return words


if __name__ == "__main__":
    dictionary = Dictionary()
    # Insert words to the dictionary
    dictionary.insert("abc")
    dictionary.insert("abd")
    dictionary.insert("abcd")
    dictionary.insert("abcd")  # add duplicated word
    dictionary.insert_words("cde", "def")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    # Search word in the dictionary
    print("Is 'abc' in dictionary: {}".format(dictionary.search("abc")))
    print("Is 'abe' in dictionary: {}".format(dictionary.search("abe")))
    print("Is 'abcd' in dictionary: {}".format(dictionary.search("abcd")))

    # List all words starting with prefix
    print("Words starting with 'abc': {}".format(dictionary.list_words_starting_with_prefix("abc")))
    print("Words starting with 'ab': {}".format(dictionary.list_words_starting_with_prefix("ab")))
    print("Words starting with 'abcd': {}".format(dictionary.list_words_starting_with_prefix("abcd")))
    print("Words starting with 'b': {}".format(dictionary.list_words_starting_with_prefix("b")))
    print("Words starting with 'c': {}".format(dictionary.list_words_starting_with_prefix("c")))
    print("Words starting with 'd': {}".format(dictionary.list_words_starting_with_prefix("d")))
