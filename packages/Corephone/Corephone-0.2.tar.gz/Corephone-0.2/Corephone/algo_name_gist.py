#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Corephone (Updated version of nameGist) Algorithm
# Version 2.0
#
# Authors:
#   Md. Mahmudul Hasan Shohag
#   imaginativeshohag@gmail.com
#
#   Mohammad Imran Hossain
#   imranhossain16.ctg@gmail.com
#
#   Shafayat Jamil
#   shafayatiuc@gmail.com
# ----------------------------------------------------------------------------
import os.path
from .algo_name_gist_uni_bn import *
from .non_unicode_to_unicode import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

vowel_mark_singles = [
    'a',  # আ-কার
    'i',  # ই-কার, ঈ-কার
    'e',  # ই-কার, ঈ-কার, এ-কার
    'y',  # ই-কার, ঈ-কার
    'u',  # উ-কার, ঊ-কার
    'o'  # ও-কার
]

vowel_mark_doubles = [

    # ----------------------------------------------------------------------------
    # Positive:
    #     k[ri]shna
    #
    # Negative:
    #     af[ri]n
    #
    # Remove Note:
    #     People will mistake to write "ri".
    #     But big chance there will be a "r" in that mistake.
    #     So, removing whole "ri" is not a good idea :)
    # ----------------------------------------------------------------------------
    # 'ri',  # ঋ-কার

    'oi',  # ঐ-কার
    'ow',  # ঔ-কার (কৌশিক - kowshik)
    'ou',  # ঔ-কার (সৌম্য - soummyo)
    'ue',  # haque (sounds like k)

    # ----------------------------------------------------------------------------
    # Add Note:
    #   sh[ei]kh, sh[e]kh
    #
    # Remove Note:
    #   Gave wrong answer then right answer
    # ----------------------------------------------------------------------------
    # 'ei',  # এই (শেখ - sheikh)

    # ----------------------------------------------------------------------------
    # Add Note:
    #   hoss[ai]n, hoss[e]n
    #
    # Remove Note:
    #   Gave wrong answer then right answer
    # ----------------------------------------------------------------------------
    # 'ai',  # এই (হোসেন/হোসাইন - hossain)
]

consonants = [
    'b',  # ব
    'c',  # চ
    'd',  # ড, দ
    'f',  # ফ
    'g',  # গ
    'h',  # হ
    'j',  # জ, য
    'k',  # ক
    'l',  # ল
    'm',  # ম
    'n',  # ণ, ন
    'p',  # প
    'q',  # ক
    'r',  # র, ড়, ঢ়
    's',  # শ, ষ, স
    't',  # ট, ত
    'v',  # ভ
    'w',  # য়
    'x',  #
    'y',  # য়
    'z',  #
]

alphabet_map = {
    'k': 'k',
    'kh': 'k',
    'q': 'k',

    # ----------------------------------------------------------------------------
    # Why g -> s? not g -> z/j/g?
    #   julhasnain, julhaznain
    #   mejbah, misbah
    #
    #   people tends to write "g", "j" instead of "s" and vice-versa,
    #   so its better to turn all to "s".
    # ----------------------------------------------------------------------------

    'g': 's',  # use S instead of Z (For Test)
    'gh': 's',  # use S instead of Z (For Test)
    'j': 's',  # use S instead of Z (For Test)
    'jh': 's',  # use S instead of Z (For Test)
    'z': 's',  # use S instead of Z (For Test)
    'zh': 's',  # use S instead of Z (For Test)
    'x': 's',  # use S instead of Z (For Test)

    # 'g': 'z',
    # 'gh': 'z',
    # 'j': 'z',
    # 'jh': 'z',
    # 'z': 'z',
    # 'zh': 'z',
    # 'x': 'z',

    'c': 's',  # use S instead of C (For Test)
    'ch': 's',  # use S instead of C (For Test)

    't': 't',
    'th': 't',

    'd': 'd',
    'dh': 'd',

    'n': 'n',

    'p': 'p',
    'ph': 'p',
    'f': 'p',

    'b': 'b',
    'bh': 'b',
    'v': 'b',

    'm': 'm',

    'r': 'r',

    'l': 'l',

    's': 's',
    'sh': 's',

    'h': 'h',

    'y': 'a',  # Faisal, Faysal
    'w': 'a',
    # 'y': 'e',  # ইয়াকুব (yakub), ইয়াসমিন (yeasmin)
    # 'w': 'o',  # ওয়াহিদ (wahid), কাওসার (kawsar)

    'a': 'a',  # য়
    'e': 'a',  # আ (আইনুল - Einul)
    'i': 'a',  # ই (ইফতেখার - Ifthekhar)
    # 'i': 'e',  # ই (ইফতেখার - Ifthekhar)
    'o': 'a',  # অ (অভি - Ovi, অর্শি - Orshi)
    'u': 'a',  # উ (উদ্দিন - Uddin)
}

# ----------------------------------------------------------------------------
# Initialize English phonetic titles and salutations
# ----------------------------------------------------------------------------
title_and_salutation_file = open(PROJECT_ROOT + '/titles_and_salutations.txt', 'r', encoding='utf-8')
title_and_salutation_list = title_and_salutation_file.read().split('\n')

# ----------------------------------------------------------------------------
# Initialize Unicode Bangla titles and salutations
# ----------------------------------------------------------------------------
uni_bn_title_and_salutation_file = open(PROJECT_ROOT + '/uni_bn_titles_and_salutations.txt', 'r', encoding='utf-8')
uni_bn_title_and_salutation_list = uni_bn_title_and_salutation_file.read().split('\n')


def name_gist_test(persons_name):
    """
    Print batch result for Test

    Example:
    name_gist_test(['name one', 'name two'])
    
    :param persons_name: list
    """
    for index in range(len(persons_name)):
        if index != 0:
            print('--------------------------------')

        print(corephone(persons_name[index], True))


def corephone(person_name, print_steps=False):
    """
    Return the significant part of any Bangla text

    Example:
    To get only the output code:
    name_gist('text')

    To view the steps of the process:
    name_gist('text', True)


    :param print_steps: bool
    :type person_name: str
    """

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # check is it Non Unicode Bangla
    # ----------------------------------------------------------------------------

    if person_name[0] == '$':
        person_name = non_uni_to_uni(person_name)

    # ----------------------------------------------------------------------------
    # check is it Unicode Bangla or English Phonetic Bangla
    # ----------------------------------------------------------------------------

    try:
       person_name.encode('ascii')
    except UnicodeEncodeError:
        return name_gist_uni_bn(person_name, print_steps)

    # ----------------------------------------------------------------------------
    # make it lowercase
    # ----------------------------------------------------------------------------
    person_name = person_name.lower()

    # ----------------------------------------------------------------------------
    # remove title and salutation
    #
    # NOTE:
    #   1. In general there only [one] title/salutation found in names
    # ----------------------------------------------------------------------------
    for title_or_salutation in title_and_salutation_list:
        title_or_sal_len = len(title_or_salutation)
        if person_name[:title_or_sal_len] == title_or_salutation:
            person_name = person_name[title_or_sal_len:]
            break  # NOTE 1

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # remove all unnecessary signs
    # ----------------------------------------------------------------------------
    person_name_len = len(person_name)
    new_person_name = ''
    for index in range(person_name_len):
        if person_name[index] != '.' and \
                person_name[index] != ':' and \
                person_name[index] != '(' and \
                person_name[index] != ')' and \
                person_name[index] != '-' and \
                person_name[index] != '\\' and \
                person_name[index] != 'ঃ':  # Bangla Bishorgo
            new_person_name += person_name[index]

    person_name = new_person_name

#    if print_steps:
#        print(person_name)

#    new_person_name = ''
#    for index in range(person_name_len):
#        if 'a' <= person_name[index] <= 'z':
#            new_person_name += person_name[index]

#    person_name = new_person_name

    person_name = person_name.strip()

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # remove vowel marks, except it is the
    # first letter or after a space
    #
    # Theory:
    # "Vowel Marks are always placed after Consonant"
    # ----------------------------------------------------------------------------

    result = ''
    found_consonant = False
    found_space = False
    person_name_len = len(person_name)
    do_skip = False

    for i in range(person_name_len):
        if do_skip:
            do_skip = False
            continue

        if i != 0:       # If current character is not first character.
            if person_name[i] == person_name[i-1]:  #If double character found then skip
                continue

        if i is 0:  # first character
            result = result + person_name[i]

            if person_name[i] in consonants:
                found_consonant = True

        elif found_space:
            found_space = False
            result = result + person_name[i]

            if person_name[i] in consonants:
                found_consonant = True

        elif person_name[i] == ' ':
            found_space = True
            found_consonant = False

        elif found_consonant:  # after found consonant, removing vowel
            if i != person_name_len - 1:
                if person_name[i] + person_name[i + 1] in vowel_mark_doubles:
                    found_consonant = False
                    do_skip = True

                elif person_name[i] in vowel_mark_singles:
                    found_consonant = False

                else:
                    result = result + person_name[i]

            elif person_name[i] in vowel_mark_singles:
                found_consonant = False

            else:
                result = result + person_name[i]

        else:
            if person_name[i] in consonants:  # is current character is a consonant?
                found_consonant = True

            result = result + person_name[i]

    person_name = result

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Replacing same sounding letters
    # E.g.: sh -> s
    # ----------------------------------------------------------------------------
    result = ''
    person_name_len = len(person_name)
    do_skip = False

    for i in range(person_name_len):

        if do_skip:
            do_skip = False
            continue

        if person_name[i] != '1':

            if i != person_name_len - 1:

                if person_name[i] + person_name[i + 1] in alphabet_map.keys() and person_name[i + 1] != '1':
                    result = result + alphabet_map[person_name[i] + person_name[i + 1]]
                    do_skip = True
                else:
                    try:
                        result = result + alphabet_map[person_name[i]]
                    except KeyError:
                        # Just ignore the character
                        if print_steps:
                            print("KeyError for character: \"" + person_name[i] + "\"")

            else:
                try:
                    result = result + alphabet_map[person_name[i]]
                except KeyError:
                    # Just ignore the character
                    if print_steps:
                        print("KeyError for character: \"" + person_name[i] + "\"")

    person_name = result

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Post-processing: remove double characters
    # ----------------------------------------------------------------------------

    result = ''
    now = ''
    length_s = len(person_name)
    for i in range(length_s):
        if person_name[i] == now:
            continue
        result = result + person_name[i]
        now = person_name[i]

#    if print_steps:
#        print(result)

    return result
