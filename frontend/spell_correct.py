# Credit for Spell Correction algorithm goes to Peter Norvig
# http://norvig.com/spell-correct.html

import shelve

NWORDS = shelve.open('spell_db')

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def dist1(word):
  deletes = []
  for i in range(len(word)):
    deletes.append(word[:i] + word[i+1:]) 

  transposes = []
  if len(word) > 1:
    for i in range(len(word) - 1):
      tr = word[:i] + word[i+1] + word[i] + word[i+2:]
      transposes.append(tr)

  replaces = []
  for i in range(len(word)):
    for letter in alphabet:
      r = word[:i] + letter + word[i+1:]
      replaces.append(r)

  inserts = []
  for i in range(len(word) + 1):
    for letter in alphabet:
      inserts.append(word[:i] + letter + word[i:])

  return set(deletes + transposes + replaces + inserts)

def known(words):
  knowns = []
  for word in words:
    if word in NWORDS:
      knowns.append(word)

  return set(knowns)

def known_dist1(word):
  return known(dist1(word))

def known_dist2(word):
  knowns = []
  for d1 in dist1(word):
    for d2 in dist1(d1):
      if d2 in NWORDS:
        knowns.append(d2)

  return set(knowns)

def correct(word):
  candidates = known([word]) or known_dist1(word) or known_dist2(word) or [word]
  return max(candidates, key=NWORDS.get)



