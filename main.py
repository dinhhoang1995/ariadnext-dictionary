import json

from typing import List


class NumberOfErrorsTooBig(Exception):
    pass


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
        node.setdefault("_end", word)

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

    def edits(self, node, word, results, depth) -> List[str]:
        if len(word) == 0 and depth >= 0 and "_end" in node and node["_end"] not in results:
            results.append(node["_end"])

        if depth >= 1:
            # # deletion (remove the current letter and try it on the current branch)
            # if depth > 1:
            #     self.edits(node, word[1:], results, depth - 1)
            # else:
            #     self.edits(node, "", results, depth - 1)

            for char, branch in node.items():
                if char == "_end":
                    continue

                # # insertion (pass the current word to each of the branches)
                # self.edits(branch, word, results, depth - 1)

                # substitution (pass the current word without the first character to each of the branches)
                if len(word) > 1:
                    self.edits(branch, word[1:], results, depth - 1)
                else:
                    self.edits(branch, "", results, depth - 1)

            # # transposition (swap the first and second characters)
            # if len(word) > 2:
            #     self.edits(node, word[1] + word[0] + word[2:], results, depth - 1)
            # elif len(word) == 2:
            #     self.edits(node, word[1] + word[0], results, depth - 1)

        # move on to the next letter (no edits have happened)
        if len(word) >= 1 and word[0] in node:
            char = word[0]
            if len(word) > 1:
                self.edits(node[char], word[1:], results, depth)
            elif len(word) == 1:
                self.edits(node[char], "", results, depth)

        return results

    def suggest_misspelled_word(self, word, number_of_errors) -> List[str]:
        """
        Suggest words in dictionary that match the misspelled word
        :param word:
        :param number_of_errors:
        :return:
        """
        if number_of_errors >= len(word):
            raise NumberOfErrorsTooBig("Number of errors must be smaller than length of word!")

        if self.search(word):
            return [word]

        return self.edits(self.root, word, [], number_of_errors)

    def validate_word(self, word, number_of_errors) -> bool:
        """
        Validate a word with words in dictionary
        :param word:
        :param number_of_errors:
        :return:
        """
        return True if len(self.suggest_misspelled_word(word, number_of_errors)) else False


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

    # Dictionary with errors
    print("Suggest words in dictionary for 'abe' with 1 error: {}".format(dictionary.suggest_misspelled_word("abe", 1)))
    print("Suggest words in dictionary for 'abc' with 1 error: {}".format(dictionary.suggest_misspelled_word("abc", 1)))
    print("Suggest words in dictionary for 'bbc' with 1 error: {}".format(dictionary.suggest_misspelled_word("bbc", 1)))
    print("Suggest words in dictionary for 'afc' with 1 error: {}".format(dictionary.suggest_misspelled_word("afc", 1)))
    print("Suggest words in dictionary for 'bbb' with 2 error: {}".format(dictionary.suggest_misspelled_word("bbb", 2)))
    print(
        "Suggest words in dictionary for 'afed' with 2 error: {}".format(dictionary.suggest_misspelled_word("afed", 2))
    )

    # Validate word
    print("Is 'abe' with 1 error valid: {}".format(dictionary.validate_word("abe", 1)))
    print("Is 'ace' with 1 error valid: {}".format(dictionary.validate_word("ace", 1)))

    try:
        print("Is 'ace' with 3 error valid: {}".format(dictionary.validate_word("ace", 3)))
    except NumberOfErrorsTooBig as e:
        print(f"Catched NumberOfErrorsTooBig Exception while validating 'ace' with 3 error valid: {e}")
