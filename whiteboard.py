#  Print out all of the strings in the following array in alphabetical order, each on a separate line.

words = [
    'Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba',
    'Paso Doble', 'Jive'
]

for word in sorted(words, key=None, reverse=False):
    print(word)