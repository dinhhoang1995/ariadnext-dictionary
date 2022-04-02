import pytest

from main import Dictionary, NumberOfErrorsTooBig, WordNotFound, EmptyString


def test_insert_word():
    dictionary = Dictionary()
    dictionary.insert("abc")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}

    with pytest.raises(EmptyString):
        dictionary.insert("")


def test_insert_duplicated_word():
    dictionary = Dictionary()
    dictionary.insert("abc")
    dictionary.insert("abc")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}


def test_insert_multi_words():
    dictionary = Dictionary()
    dictionary.insert_words("abc", "abd", "cde")
    assert dictionary.get_dictionary() == {
        "a": {"b": {"c": {"_end": "abc"}, "d": {"_end": "abd"}}},
        "c": {"d": {"e": {"_end": "cde"}}},
    }


def test_search_word():
    dictionary = Dictionary()
    dictionary.insert("abc")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}
    assert dictionary.search("abc")
    assert not dictionary.search("abe")


def test_list_all_words_starting_with_prefix():
    dictionary = Dictionary()
    dictionary.insert_words("abc", "abd", "cde")
    assert dictionary.get_dictionary() == {
        "a": {"b": {"c": {"_end": "abc"}, "d": {"_end": "abd"}}},
        "c": {"d": {"e": {"_end": "cde"}}},
    }
    assert dictionary.list_words_starting_with_prefix("abc") == ["abc"]
    assert dictionary.list_words_starting_with_prefix("ab") == ["abc", "abd"]
    assert dictionary.list_words_starting_with_prefix("c") == ["cde"]
    assert dictionary.list_words_starting_with_prefix("b") == []


def test_suggest_misspelled_word():
    dictionary = Dictionary()
    dictionary.insert_words("abc", "abd", "cde", "xyzt")
    assert dictionary.get_dictionary() == {
        "a": {"b": {"c": {"_end": "abc"}, "d": {"_end": "abd"}}},
        "c": {"d": {"e": {"_end": "cde"}}},
        "x": {"y": {"z": {"t": {"_end": "xyzt"}}}},
    }
    assert dictionary.suggest_misspelled_word("abc", 1) == ["abc"]
    assert dictionary.suggest_misspelled_word("abe", 1) == ["abc", "abd"]
    assert dictionary.suggest_misspelled_word("bbb", 2) == ["abc", "abd"]
    assert dictionary.suggest_misspelled_word("cc", 1) == []
    assert dictionary.suggest_misspelled_word("fff", 2) == []
    assert dictionary.suggest_misspelled_word("xyzz", 1) == ["xyzt"]
    assert dictionary.suggest_misspelled_word("xywz", 1) == []
    assert dictionary.suggest_misspelled_word("xywz", 2) == ["xyzt"]

    with pytest.raises(NumberOfErrorsTooBig):
        dictionary.suggest_misspelled_word("bbb", 3)


def test_validate_word():
    dictionary = Dictionary()
    dictionary.insert_words("abc", "abd", "cde", "xyzt")
    assert dictionary.get_dictionary() == {
        "a": {"b": {"c": {"_end": "abc"}, "d": {"_end": "abd"}}},
        "c": {"d": {"e": {"_end": "cde"}}},
        "x": {"y": {"z": {"t": {"_end": "xyzt"}}}},
    }
    assert dictionary.validate_word("abc", 1)
    assert dictionary.validate_word("abe", 1)
    assert dictionary.validate_word("bbb", 2)
    assert not dictionary.validate_word("cc", 1)
    assert not dictionary.validate_word("fff", 2)
    assert dictionary.validate_word("xyzz", 1)
    assert not dictionary.validate_word("xywz", 1)
    assert dictionary.validate_word("xywz", 2)

    with pytest.raises(NumberOfErrorsTooBig):
        dictionary.validate_word("bbb", 3)


def test_delete_word():
    dictionary = Dictionary()
    dictionary.insert_words("abc", "abd")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}, "d": {"_end": "abd"}}}}

    dictionary.remove("abd")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}

    dictionary.remove("abe")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}


def test_update_word():
    dictionary = Dictionary()
    dictionary.insert("abc")
    assert dictionary.get_dictionary() == {"a": {"b": {"c": {"_end": "abc"}}}}

    dictionary.update("abc", "ab")  # remove a character
    assert dictionary.get_dictionary() == {"a": {"b": {"_end": "ab"}}}

    dictionary.update("ab", "akb")  # add a character
    assert dictionary.get_dictionary() == {"a": {"k": {"b": {"_end": "akb"}}}}

    dictionary.update("akb", "akt")  # update a character
    assert dictionary.get_dictionary() == {"a": {"k": {"t": {"_end": "akt"}}}}

    with pytest.raises(WordNotFound):
        dictionary.update("xyz", "xxx")
