#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Part of the Corephone (Updated version of nameGist) Algorithm
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
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

uni_alphabet_map = {
    'অ': 'a',
    'আ': 'a',
    'ই': 'a',
    'ঈ': 'a',
    'উ': 'a',
    'ঊ': 'a',
    'ঋ': 'a',
    'এ': 'a',
    'ঐ': 'a',
    'ও': 'a',
    'ঔ': 'a',

    'ক': 'k',
    'খ': 'k',
    'গ': 's',
    'ঘ': 's',
    'ঙ': '',  # null
    'চ': 's',
    'ছ': 's',
    'জ': 's',
    'ঝ': 's',
    'ঞ': '',  # null
    'ট': 't',
    'ঠ': 't',
    'ড': 'd',
    'ঢ': 'd',
    'ণ': 'n',
    'ত': 't',
    'থ': 't',
    'দ': 'd',
    'ধ': 'd',
    'ন': 'n',
    'প': 'p',
    'ফ': 'p',
    'ব': 'b',
    'ভ': 'b',
    'ম': 'm',
    'য': 's',
    'র': 'r',
    'ল': 'l',
    'শ': 's',
    'ষ': 's',
    'স': 's',
    'হ': 'h',
    'ড়': 'r',
    'ঢ়': 'r',
    'য়': 'a',
    'ৎ': 't',
    'ং': '',  # null
    'ঃ': '',  # null
    'ঁ': '',  # null
    '্': '',  # null
}

# ----------------------------------------------------------------------------
# Initialize Unicode Bangla titles and salutations
# ----------------------------------------------------------------------------
uni_bn_title_and_salutation_file = open(PROJECT_ROOT + '/uni_bn_titles_and_salutations.txt', 'r', encoding='utf-8')
uni_bn_title_and_salutation_list = uni_bn_title_and_salutation_file.read().split('\n')


def name_gist_uni_bn(person_name, print_steps=False):

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # remove Bangla title and salutation
    #
    # NOTE:
    #   1. In general there only [one] title/salutation found in names
    # ----------------------------------------------------------------------------
    for title_or_salutation in uni_bn_title_and_salutation_list:
        # person_name = person_name.replace(title_or_salutation, '')
        title_or_sal_len = len(title_or_salutation)
        if person_name[:title_or_sal_len] == title_or_salutation:
            person_name = person_name[title_or_sal_len:]
            break  # NOTE 1

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Remove Unnecessary Symbols
    # ----------------------------------------------------------------------------
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

        #if 'ঀ' <= person_name[index] <= '৾':
        #    # Source: https://en.wikipedia.org/wiki/Bengali_(Unicode_block)
        #    new_person_name += person_name[index]

    person_name = new_person_name

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # remove start-end spaces
    # ----------------------------------------------------------------------------
    person_name = person_name.strip()

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Remove Vowel Marks and space
    # ----------------------------------------------------------------------------
    new_person_name = ''
    for item in person_name:
        if item != 'া' and \
                item != 'ি' and \
                item != 'ী' and \
                item != 'ু' and \
                item != 'ূ' and \
                item != 'ে' and \
                item != 'ৈ' and \
                item != 'ো' and \
                item != 'ৌ' and \
                item != ' ':
            new_person_name += item

    person_name = new_person_name

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Replacing same sounding letters
    # ----------------------------------------------------------------------------
    new_person_name = ''
    for item in person_name:
        try:
            new_person_name += uni_alphabet_map[item]
        except KeyError:
            # Just ignore the character
            if print_steps:
                print("KeyError for character: \"" + item + "\"")

    person_name = new_person_name

#    if print_steps:
#        print(person_name)

    # ----------------------------------------------------------------------------
    # Post-processing: remove double characters
    # ----------------------------------------------------------------------------
    result = ''
    now = ''
    for i in range(len(person_name)):
        if person_name[i] == now:
            continue
        result = result + person_name[i]
        now = person_name[i]

    person_name = result

#    if print_steps:
#        print(person_name)

    return person_name