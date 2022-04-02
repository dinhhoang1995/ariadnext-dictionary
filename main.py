import json

from typing import List


class NumberOfErrorsTooBig(Exception):
    pass


class WordNotFound(Exception):
    pass


class EmptyString(Exception):
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
        Insert multi words
        :param words:
        :return:
        """
        for word in words:
            self.insert(word)

    def insert(self, word: str):
        """
        Insert a word
        :param word:
        :return:
        """
        if len(word) == 0:
            raise EmptyString("Word cannot be empty!")

        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node.setdefault("_end", word)

    def search(self, word: str) -> bool:
        """
        Search a word
        :param word:
        :return: True if the word is found else False
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

    def list_words_starting_with_prefix(self, prefix: str) -> List[str]:
        """
        List all words starting with the prefix
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

    def _edits(self, node, word, results, depth) -> List[str]:
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
                    self._edits(branch, word[1:], results, depth - 1)
                else:
                    self._edits(branch, "", results, depth - 1)

            # # transposition (swap the first and second characters)
            # if len(word) > 2:
            #     self.edits(node, word[1] + word[0] + word[2:], results, depth - 1)
            # elif len(word) == 2:
            #     self.edits(node, word[1] + word[0], results, depth - 1)

        # move on to the next letter (no edits have happened)
        if len(word) >= 1 and word[0] in node:
            char = word[0]
            if len(word) > 1:
                self._edits(node[char], word[1:], results, depth)
            elif len(word) == 1:
                self._edits(node[char], "", results, depth)

        return results

    def suggest_misspelled_word(self, word: str, number_of_errors: int) -> List[str]:
        """
        Suggest words that match the misspelled word
        :param word:
        :param number_of_errors:
        :return:
        """
        if number_of_errors >= len(word):
            raise NumberOfErrorsTooBig("Number of errors must be smaller than the length of word!")

        if self.search(word):
            return [word]

        return self._edits(self.root, word, [], number_of_errors)

    def validate_word(self, word: str, number_of_errors: int) -> bool:
        """
        Validate a word
        :param word:
        :param number_of_errors:
        :return:
        """
        return True if len(self.suggest_misspelled_word(word, number_of_errors)) else False

    def remove(self, word: str):
        """
        Remove a word
        :param word:
        :return:
        """
        self._delete(self.root, word, 0)

    def _delete(self, node, word, idx) -> bool:
        if len(word) == idx:
            if "_end" in node and node["_end"] == word:
                del node["_end"]
                return True
            else:
                return False
        else:
            char = word[idx]
            if char in node and self._delete(node[char], word, idx + 1):
                # Remove empty node
                if len(node[char]) == 0:
                    del node[char]
                    return True
                else:
                    return False

            else:
                return False

    def update(self, current_word: str, new_word: str):
        """
        Update a word
        :param current_word:
        :param new_word:
        :return:
        """
        if not self.search(current_word):
            raise WordNotFound("Cannot found the current word in the dictionary!")

        self.remove(current_word)
        self.insert(new_word)


if __name__ == "__main__":
    dictionary = Dictionary()
    # Insert words to the dictionary
    print("=============================== Insert words to the dictionary ============================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    print("Insert 'abc'")
    dictionary.insert("abc")

    print("Insert 'abd'")
    dictionary.insert("abd")

    print("Insert 'abcd'")
    dictionary.insert("abcd")

    print("Insert 'abcd'")
    dictionary.insert("abcd")  # add duplicated word

    print("Insert 'cde' and 'def'")
    dictionary.insert_words("cde", "def")

    try:
        print("Insert ''...")
        dictionary.insert("")
    except EmptyString as e:
        print(f"Caught EmptyString Exception while inserting '': {e}")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    # Search a word in the dictionary
    print("================================== Search a word in the dictionary ========================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))
    print("Is 'abc' in the dictionary: {}".format(dictionary.search("abc")))
    print("Is 'abe' in the dictionary: {}".format(dictionary.search("abe")))
    print("Is 'abcd' in the dictionary: {}".format(dictionary.search("abcd")))

    # List all words starting with prefix
    print("================================= List all words starting with prefix =====================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))
    print("Words starting with 'abc': {}".format(dictionary.list_words_starting_with_prefix("abc")))
    print("Words starting with 'ab': {}".format(dictionary.list_words_starting_with_prefix("ab")))
    print("Words starting with 'abcd': {}".format(dictionary.list_words_starting_with_prefix("abcd")))
    print("Words starting with 'b': {}".format(dictionary.list_words_starting_with_prefix("b")))
    print("Words starting with 'c': {}".format(dictionary.list_words_starting_with_prefix("c")))
    print("Words starting with 'd': {}".format(dictionary.list_words_starting_with_prefix("d")))

    # Dictionary with errors
    print("========================= List all suggested words for a misspelled word ==================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))
    print("Suggested words for 'abe' with 1 error: {}".format(dictionary.suggest_misspelled_word("abe", 1)))
    print("Suggested words for 'abc' with 1 error: {}".format(dictionary.suggest_misspelled_word("abc", 1)))
    print("Suggested words for 'bbc' with 1 error: {}".format(dictionary.suggest_misspelled_word("bbc", 1)))
    print("Suggested words for 'afc' with 1 error: {}".format(dictionary.suggest_misspelled_word("afc", 1)))
    print("Suggested words for 'bbb' with 2 error: {}".format(dictionary.suggest_misspelled_word("bbb", 2)))
    print("Suggested words for 'afed' with 2 error: {}".format(dictionary.suggest_misspelled_word("afed", 2)))

    try:
        print("Suggested words for 'bbb' with 3 error...")
        dictionary.suggest_misspelled_word("bbb", 3)
    except NumberOfErrorsTooBig as e:
        print(f"Caught NumberOfErrorsTooBig Exception while listing suggested words for 'bbb' with 3 error: {e}")

    # Validate a word
    print("========================================= Validate a word =================================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))
    print("Is 'abe' with 1 error valid: {}".format(dictionary.validate_word("abe", 1)))
    print("Is 'ace' with 1 error valid: {}".format(dictionary.validate_word("ace", 1)))

    try:
        print("Is 'ace' with 3 error valid...")
        dictionary.validate_word("ace", 3)
    except NumberOfErrorsTooBig as e:
        print(f"Caught NumberOfErrorsTooBig Exception while validating 'ace' with 3 error valid: {e}")

    # Delete a word
    print("=========================================== Delete a word =================================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    print("Remove 'cde' from the dictionary")
    dictionary.remove("cde")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    # Update a word
    print("============================================= Update a word ===============================================")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    print("Update 'def' to 'de'")
    dictionary.update("def", "de")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    print("Update 'de' to 'deg'")
    dictionary.update("de", "deg")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))

    try:
        print("Update 'xyz' to 'xyt'...")
        dictionary.update("xyz", "xyt")
    except WordNotFound as e:
        print(f"Caught WordNotFound Exception while updating 'xyz' to 'xyt': {e}")
    print("Current dictionary status:\n{}".format(json.dumps(dictionary.get_dictionary(), sort_keys=True, indent=4)))
