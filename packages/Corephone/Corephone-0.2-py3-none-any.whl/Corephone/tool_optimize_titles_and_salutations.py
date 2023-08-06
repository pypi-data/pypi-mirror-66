# ----------------------------------------------------------------------------
# This tool make all word lower case (for English Phonetic)
# and sort the words descending based on their length.
#
# Version 2.0
#
# Authors:
#   Md. Mahmudul Hasan Shohag
#   imaginativeshohag@gmail.com
#
#   Mohammad Imran Hossain
#   imranhossain16.ctg@gmail.com
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# For English Phonetic
# ----------------------------------------------------------------------------

file = open('titles_and_salutations.txt', 'r')

data = file.read().split('\n')

file.close()

result = set()

# ----------------------------------------------------------------------------
# Make all lower case and take only unique ones
# ----------------------------------------------------------------------------
for item in data:
    result.add(item.lower())

result = list(result)

# ----------------------------------------------------------------------------
# Sort the name in descending
# order based on the words length
# ----------------------------------------------------------------------------
result.sort(key=lambda s: len(s), reverse=True)

print(result)

file.close()

file = open('titles_and_salutations.txt', 'w')

is_first = True

for item in result:
    if is_first:
        is_first = False
    else:
        file.write('\n')

    file.write(item)

file.close()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# For Bangla Unicode
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

file = open('uni_bn_titles_and_salutations.txt', 'r')

data = file.read().split('\n')

file.close()

result = set()

# ----------------------------------------------------------------------------
# Take only unique ones
# ----------------------------------------------------------------------------
for item in data:
    result.add(item)

result = list(result)

# ----------------------------------------------------------------------------
# Sort the name in descending
# order based on the words length
# ----------------------------------------------------------------------------
result.sort(key=lambda s: len(s), reverse=True)

print(result)

file.close()

file = open('uni_bn_titles_and_salutations.txt', 'w')

is_first = True

for item in result:
    if is_first:
        is_first = False
    else:
        file.write('\n')

    file.write(item)

file.close()
