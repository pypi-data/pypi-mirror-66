#!/usr/bin/env python
# encoding: utf-8


import re

hiraganaDict = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "ん": "n",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "きゃ": "kya",
    "きゅ": "kyu",
    "きぇ": "kye",
    "きょ": "kyo",
    "さ": "sa",
    "すぃ": "si",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "しゃ": "sha",
    "し": "shi",
    "しゅ": "shu",
    "しぇ": "she",
    "しょ": "sho",
    "た": "ta",
    "てぃ": "ti",
    "てぅ": "tu",
    "て": "te",
    "と": "to",
    "ちゃ": "cha",
    "ち": "chi",
    "ちゅ": "chu",
    "ちぇ": "che",
    "ちょ": "cho",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "にゃ": "nya",
    "にゅ": "nyu",
    "にぇ": "nye",
    "にょ": "nyo",
    "は": "ha",
    "ひ": "hi",
    "ほぅ": "hu",
    "へ": "he",
    "ほ": "ho",
    "ひゃ": "hya",
    "ひゅ": "hyu",
    "ひぇ": "hye",
    "ひょ": "hyo",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "みゃ": "mya",
    "みゅ": "myu",
    "みぇ": "mye",
    "みょ": "myo",
    "や": "ya",
    "いぃ": "yi",
    "ゆ": "yu",
    "いぇ": "ye",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "りゃ": "rya",
    "りゅ": "ryu",
    "りぇ": "rye",
    "りょ": "ryo",
    "わ": "wa",
    "うぃ": "wi",
    "ゐ": "wi",
    "うぅ": "wu",
    "うぇ": "we",
    "ゑ": "we",
    "を": "wo",
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "ぎゃ": "gya",
    "ぎゅ": "gyu",
    "ぎぇ": "gye",
    "ぎょ": "gyo",
    "ざ": "za",
    "ずぃ": "zi",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "じゃ": "ja",
    "じ": "ji",
    "じゅ": "ju",
    "じぇ": "je",
    "じょ": "jo",
    "だ": "da",
    "でぃ": "di",
    "ぢ": "di",
    "でぅ": "du",
    "づ": "du",
    "で": "de",
    "ど": "do",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "びゃ": "bya",
    "びゅ": "byu",
    "びぇ": "bye",
    "びょ": "byo",
    "ぴゃ": "pya",
    "ぴゅ": "pyu",
    "ぴぇ": "pye",
    "ぴょ": "pyo",
    "ヴぁ": "va",
    "ヴぃ": "vi",
    "ヴ": "vu",
    "ヴぇ": "ve",
    "ヴぉ": "vo",
    "_": "_",
    "__": "__",
    "つぁ": "tsa",
    "つぃ": "tsi",
    "つ": "tsu",
    "つぇ": "tse",
    "つぉ": "tso",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    "ふぁ": "fa",
    "ふぃ": "fi",
    "ふ": "fu",
    "ふぇ": "fe",
    "ふぉ": "fo"

}

romajiDict = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "n": "ん",
    "ka": "か",
    "ki": "き",
    "ku": "く",
    "ke": "け",
    "ko": "こ",
    "kya": "きゃ",
    "kyu": "きゅ",
    "kye": "きぇ",
    "kyo": "きょ",
    "sa": "さ",
    "si": "すぃ",
    "su": "す",
    "se": "せ",
    "so": "そ",
    "sha": "しゃ",
    "shi": "し",
    "shu": "しゅ",
    "she": "しぇ",
    "sho": "しょ",
    "ta": "た",
    "ti": "てぃ",
    "tu": "てぅ",
    "te": "て",
    "to": "と",
    "cha": "ちゃ",
    "chi": "ち",
    "chu": "ちゅ",
    "che": "ちぇ",
    "cho": "ちょ",
    "na": "な",
    "ni": "に",
    "nu": "ぬ",
    "ne": "ね",
    "no": "の",
    "nya": "にゃ",
    "nyu": "にゅ",
    "nye": "にぇ",
    "nyo": "にょ",
    "ha": "は",
    "hi": "ひ",
    "hu": "ほぅ",
    "he": "へ",
    "ho": "ほ",
    "hya": "ひゃ",
    "hyu": "ひゅ",
    "hye": "ひぇ",
    "hyo": "ひょ",
    "ma": "ま",
    "mi": "み",
    "mu": "む",
    "me": "め",
    "mo": "も",
    "mya": "みゃ",
    "myu": "みゅ",
    "mye": "みぇ",
    "myo": "みょ",
    "ya": "や",
    "yi": "いぃ",
    "yu": "ゆ",
    "ye": "いぇ",
    "yo": "よ",
    "ra": "ら",
    "ri": "り",
    "ru": "る",
    "re": "れ",
    "ro": "ろ",
    "rya": "りゃ",
    "ryu": "りゅ",
    "rye": "りぇ",
    "ryo": "りょ",
    "wa": "わ",
    "wi": "うぃ",
    "wu": "うぅ",
    "we": "うぇ",
    "wo": "を",
    "ga": "が",
    "gi": "ぎ",
    "gu": "ぐ",
    "ge": "げ",
    "go": "ご",
    "gya": "ぎゃ",
    "gyu": "ぎゅ",
    "gye": "ぎぇ",
    "gyo": "ぎょ",
    "za": "ざ",
    "zi": "ずぃ",
    "zu": "ず",
    "ze": "ぜ",
    "zo": "ぞ",
    "ja": "じゃ",
    "ji": "じ",
    "ju": "じゅ",
    "je": "じぇ",
    "jo": "じょ",
    "da": "だ",
    "du": "でぅ",
    "de": "で",
    "do": "ど",
    "ba": "ば",
    "bi": "び",
    "bu": "ぶ",
    "be": "べ",
    "bo": "ぼ",
    "bya": "びゃ",
    "byu": "びゅ",
    "bye": "びぇ",
    "byo": "びょ",
    "pya": "ぴゃ",
    "pyu": "ぴゅ",
    "pye": "ぴぇ",
    "pyo": "ぴょ",
    "_": "_",
    "__": "__",
    "va": "ヴぁ",
    "vi": "ヴぃ",
    "vu": "ヴ",
    "ve": "ヴぇ",
    "vo": "ヴぉ",
    "tsa": "つぁ",
    "tsi": "つぃ",
    "tsu": "つ",
    "tse": "つぇ",
    "tso": "つぉ",
    "pa": "ぱ",
    "pi": "ぴ",
    "pu": "ぷ",
    "pe": "ぺ",
    "po": "ぽ",
    "fa": "ふぁ",
    "fi": "ふぃ",
    "fu": "ふ",
    "fe": "ふぇ",
    "fo": "ふぉ"

}

# TODO add less common hiragana that is used for extra sounds


def init_pattern(elements):
    """init_pattern(list) -> string

    Creates pattern from list sorted by length in descending order.

    """
    items = sorted(elements, key=lambda a: len(a), reverse=True)
    pattern = '|'.join(items)
    return pattern


# pattern for matching romaji
rompat = init_pattern(romajiDict.keys())
# pattern for matching hiragana
hirpat = init_pattern(hiraganaDict.keys())

# consonant regex
consonants = "ckgszjtdhfpbmyrwxnv"
conpat = "[%s]" % (consonants,)
conre = re.compile(r"^%s$" % (conpat,))


def isconsonant(char):
    """isconsonant(string) -> bool

    Returns true if string is a consonant.
    """
    if len(char) == 1 and char in "ckgszjtdhfpbmyrwxnv":
        return True
    return False


# vowel regex
vowels = "aeiou"
vowpat = "[%s]" % (vowels,)
vowre = re.compile(r"^%s$" % (vowpat,))


def isvowel(char):
    """isvowel(string) -> bool

    Returns true if string is a vowel.
    """
    if len(char) == 1 and char in 'aeiou':
        return True
    return False


n_re = re.compile(r"n'(?=[^aiueoyn]|$)")

# UTF-8 kana codes (i kept ascii because i'm not sure why it's there)
CHAR = "(?:[\x00-\x7f]|(?:\xe3\x82[\x81-\xbf])|(?:\xe3\x83[\x80-\xbc]))"

# Romaji -> Hiragana
cr_re = re.compile(r"(%s*?)(%s)" % (CHAR, rompat,))


def romgan(word):
    """romgan(string) -> string

    Converts romaji sequence into hiragana.

    """
    word = cr_re.sub(lambda m: m.groups()[0] + romajiDict[m.groups()[1]], word)
    return word


# Hiragana -> Romaji
ck_re = re.compile(r"(%s*?)(%s)" % (CHAR, hirpat,))


def ganrom(word):
    """ganrom(string) -> string
    Converts hiragana string into romaji string.
    """
    word = ck_re.sub(lambda m: m.groups()[0] + hiraganaDict[m.groups()[1]], word)
    return word
