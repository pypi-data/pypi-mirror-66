# ----------------------------------------------------------------------------
# Bangla Unicode to English Phonetic Converter
# Part of Corephone (Updated version of nameGist) Algorithm
# Version 2.0
#
# Authors:
#
#   Mohammad Imran Hossain
#   imranhossain16.ctg@gmail.com
#
#   Md. Mahmudul Hasan Shohag
#   imaginativeshohag@gmail.com
# ----------------------------------------------------------------------------

from .vars_uni_bn_to_en_phonetic import *

# todo: instead of checking the whole list, we can do this
#
# aux_alphabet = {"া": 1, "ি": 1, "ী": 1, "ু": 1, "ূ": 1, "ৃ": 1, "ে": 1, "ৈ": 1, "ো": 1, "ৌ": 1, "্য": 1, "্": 1,
#                 "্র": 1}
# real_alphabet = {"অ": 1, "আ": 1, "ই": 1, "ঈ": 1, "উ": 1, "ঊ": 1, "ঋ": 1, "এ": 1, "ঐ": 1, "ও": 1, "ঔ": 1,
#
#                  "ক": 1, "খ": 1, "গ": 1, "ঘ": 1, "ঙ": 1, "চ": 1, "ছ": 1, "জ": 1, "ঝ": 1, "ঞ": 1,
#                  "ট": 1, "ঠ": 1, "ড": 1, "ঢ": 1, "ণ": 1, "ত": 1, "থ": 1, "দ": 1, "ধ": 1, "ন": 1,
#                  "প": 1, "ফ": 1, "ব": 1, "ভ": 1, "ম": 1, "য": 1, "র": 1, "ল": 1, "শ": 1, "ষ": 1,
#                  "স": 1, "হ": 1, "ড়": 1, "ঢ়": 1, "ঢ়": 1, "ৎ": 1
#                  }

aux_alphabet = [
    aux_a,
    aux_i,
    aux_ee,
    aux_u,
    aux_uu,
    aux_ri,
    aux_e,
    aux_oi,
    aux_o,
    aux_ow,
    aux_hosonto
]

vowel_alphabet = [
    vowel_sorio_o,
    vowel_a,
    vowel_i,
    vowel_dirghi,
    vowel_ros_u,
    vowel_dirgh_u,
    vowel_ri,
    vowel_e,
    vowel_oi,
    vowel_o,
    vowel_o_oi
]

real_alphabet = [
    conso_ko,
    conso_kho,
    conso_go,
    conso_gho,
    conso_ng,
    conso_co,
    conso_cho,
    conso_jo,
    conso_jho,
    conso_nng,
    conso_to,
    conso_tho,
    conso_dalim_do,
    conso_dhol_er_dho,
    conso_mordhanno,
    conso_tal_er_to,
    conso_thetla_tho,
    conso_d,
    conso_dho,
    conso_no,
    conso_po,
    conso_fo,
    conso_bo,
    conso_vo,
    conso_mo,
    conso_zo,
    conso_ro,
    conso_lo,
    conso_talobbo_sho,
    conso_mordhanno_sho,
    conso_donto_so,
    conso_ho,
    conso_Robin_ro,
    conso_dhobin_ro,
    conso_onthosto_o,

    vowel_sorio_o,
    vowel_a,
    vowel_i,
    vowel_dirghi,
    vowel_ros_u,
    vowel_dirgh_u,
    vowel_ri,
    vowel_e,
    vowel_oi,
    vowel_o,
    vowel_o_oi
]

# todo: these hard coded bangla alphabet can be replaced by variables from variable.py

alpha_mapper = {
    "অ": map_vowel_sori_o, "আ": map_vowel_a,
    "ই": map_vowel_i, "ঈ": map_vowel_e,
    "উ": map_vowel_ros_u, "ঊ": map_vowel_dirgh_u,
    "ঋ": map_vowel_ri,
    "এ": map_vowel_e, "ঐ": map_vowel_oi,
    "ও": map_vowel_o, "ঔ": map_vowel_o_oi,

    "ক": map_conso_ko, "খ": map_conso_kho, "গ": map_conso_go, "ঘ": map_conso_gho, "ঙ": map_conso_ng,
    "চ": map_conso_co, "ছ": map_conso_cho, "জ": map_conso_jo, "ঝ": map_conso_jho, "ঞ": map_conso_nng,
    "ট": map_conso_to, "ঠ": map_conso_tho, "ড": map_conso_dalim_do, "ঢ": map_conso_dhol_er_dho, "ণ": map_conso_no,
    "ত": map_conso_tal_er_to, "থ": map_conso_thetla_tho, "দ": map_conso_do, "ধ": map_conso_dho, "ন": map_conso_no,
    "প": map_conso_po, "ফ": map_conso_fo, "ব": map_conso_bo, "ভ": map_conso_vo, "ম": map_conso_mo,
    "য": map_conso_jo, "র": map_conso_ro, "ল": map_conso_lo,
    "শ": map_conso_talobbo_sho, "ষ": map_conso_mordhanno_sho, "স": map_conso_donto_so, "হ": map_conso_ho,
    "ড়": map_conso_Robin_ro, "ঢ়": map_conso_dhobin_ro, "য়": map_conso_onthosto_o
}

aux_mapper = {
    aux_a: map_aux_a,
    aux_i: map_aux_i,
    aux_ee: map_aux_ee,
    aux_u: map_aux_u,
    aux_uu: map_aux_uu,
    aux_ri: map_aux_ri,
    aux_e: map_aux_e,
    aux_oi: map_aux_oi,
    aux_o: map_aux_o,
    aux_ow: map_aux_ow,
    aux_hosonto: map_aux_hosonto
}


def uni_bn_to_en_phonetic(person_name, print_steps=False):
    """
    Return the Phonetic English of the Unicode Bangla Text

    Example:
    To get only the output phonetic english:
    change_to_bangla('text')

    To view the steps of the process:
    change_to_bangla('text', True)


    :param print_steps: bool
    :type person_name: str
    """

    changed_name = ""

    # ----------------------------------------------------------------------------
    # Split the words from person_name using space (" ").
    # ----------------------------------------------------------------------------
    split_list = person_name.split()

    if print_steps:
        print(split_list)

    for name in split_list:

        landing_value_alert = False
        length = len(name)
        for index in range(0, length):

            value = ""
            next_value = ""
            char = name[index]

            if print_steps:
                print(char)

            # ----------------------------------------------------------------------------
            # we will only deal with the real alphabet,
            # and check if there is an aux_vowel_mark next to it.
            # ----------------------------------------------------------------------------
            if char in real_alphabet:

                # ----------------------------------------------------------------------------
                # যদি "য" পাওয়া যার এবং এর আগের ইনডেক্স এ হসন্ত থাকে, তবে য-ফলা
                # ----------------------------------------------------------------------------
                if char == conso_zo:
                    if name[index - 1] == aux_hosonto:
                        last_value = name[index - 2]
                        changed_name += alpha_mapper[last_value]
                    continue

                value = alpha_mapper[char]

                if print_steps:
                    print("Char: " + char + " | Value: " + value)

                if index + 1 < length:
                    next_value = name[index + 1]
                else:
                    landing_value_alert = True

                # ----------------------------------------------------------------------------
                # if found vowel mark, strip the value and add proper word from mapper with it.
                # if its hosonto, that means jukto borno, so leave it.
                # ----------------------------------------------------------------------------

                if next_value in aux_alphabet:

                    value = value[:-1]
                    value = value + aux_mapper[next_value]

                    if not next_value == aux_hosonto:  # hosonto hole dorkar nai
                        landing_value_alert = True
                    else:
                        landing_value_alert = False

                    changed_name += value

                else:

                    if landing_value_alert and char not in vowel_alphabet:
                        if len(value) > 1:
                            value = value[:-1]

                        landing_value_alert = False
                        changed_name += value

                    else:  # None
                        changed_name += value

                if print_steps:
                    print(changed_name)

        changed_name += " "

    if print_steps:
        print(changed_name)

    return changed_name
