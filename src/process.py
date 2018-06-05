'''
<s>	sil
eight	ey t sp
five	f ay v sp
four	f ao r sp
nine	n ay n sp
oh	ow sp
one	w ah n sp
seven	s eh v ah n sp
six	s ih k s sp
three	th r iy sp
two	t uw sp
zero	z ih r ow sp
zero	z iy r ow sp
'''

import re

f = open("../output.txt", "r")
raw = f.read()
f.close()

raw = raw.replace(
"""
2 ey eight
3 ey eight
4 ey eight
2 t eight
3 t eight
4 t eight
2 sp eight
""".strip()
, "eight")

raw = raw.replace(
"""
2 ey eight
3 ey eight
4 ey eight
2 t eight
3 t eight
4 t eight
""".strip()
, "eight")

raw = raw.replace(
"""
2 f five
3 f five
4 f five
2 ay five
3 ay five
4 ay five
2 v five
3 v five
4 v five
2 sp five
""".strip()
, "five")

raw = raw.replace(
"""
2 f five
3 f five
4 f five
2 ay five
3 ay five
4 ay five
2 v five
3 v five
4 v five
""".strip()
, "five")

raw = raw.replace(
"""
2 f four
3 f four
4 f four
2 ao four
3 ao four
4 ao four
2 r four
3 r four
4 r four
2 sp four
""".strip()
, "four")

raw = raw.replace(
"""
2 f four
3 f four
4 f four
2 ao four
3 ao four
4 ao four
2 r four
3 r four
4 r four
""".strip()
, "four")

raw = raw.replace(
"""
2 n nine
3 n nine
4 n nine
2 ay nine
3 ay nine
4 ay nine
2 n nine
3 n nine
4 n nine
2 sp nine
""".strip()
, "nine")

raw = raw.replace(
"""
2 n nine
3 n nine
4 n nine
2 ay nine
3 ay nine
4 ay nine
2 n nine
3 n nine
4 n nine
""".strip()
, "nine")

raw = raw.replace(
"""
2 w one
3 w one
4 w one
2 ah one
3 ah one
4 ah one
2 n one
3 n one
4 n one
2 sp one
""".strip()
, "one")

raw = raw.replace(
"""
2 w one
3 w one
4 w one
2 ah one
3 ah one
4 ah one
2 n one
3 n one
4 n one
""".strip()
, "one")

raw = raw.replace(
"""
2 s seven
3 s seven
4 s seven
2 eh seven
3 eh seven
4 eh seven
2 v seven
3 v seven
4 v seven
2 ah seven
3 ah seven
4 ah seven
2 n seven
3 n seven
4 n seven
2 sp seven
""".strip()
, "seven")

raw = raw.replace(
"""
2 s seven
3 s seven
4 s seven
2 eh seven
3 eh seven
4 eh seven
2 v seven
3 v seven
4 v seven
2 ah seven
3 ah seven
4 ah seven
2 n seven
3 n seven
4 n seven
""".strip()
, "seven")

raw = raw.replace(
"""
2 s six
3 s six
4 s six
2 ih six
3 ih six
4 ih six
2 k six
3 k six
4 k six
2 s six
3 s six
4 s six
2 sp six
""".strip()
, "six")

raw = raw.replace(
"""
2 s six
3 s six
4 s six
2 ih six
3 ih six
4 ih six
2 k six
3 k six
4 k six
2 s six
3 s six
4 s six
""".strip()
, "six")

raw = raw.replace(
"""
2 th three
3 th three
4 th three
2 r three
3 r three
4 r three
2 iy three
3 iy three
4 iy three
2 sp three
""".strip()
, "three")

raw = raw.replace(
"""
2 th three
3 th three
4 th three
2 r three
3 r three
4 r three
2 iy three
3 iy three
4 iy three
""".strip()
, "three")

raw = raw.replace(
"""
2 t two
3 t two
4 t two
2 uw two
3 uw two
4 uw two
2 sp two
""".strip()
, "two")

raw = raw.replace(
"""
2 t two
3 t two
4 t two
2 uw two
3 uw two
4 uw two
""".strip()
, "two")

raw = raw.replace(
"""
2 z zero
3 z zero
4 z zero
2 ih zero
3 ih zero
4 ih zero
2 r zero
3 r zero
4 r zero
2 ow zero
3 ow zero
4 ow zero
2 sp zero
""".strip()
, "zero")

raw = raw.replace(
"""
2 z zero
3 z zero
4 z zero
2 ih zero
3 ih zero
4 ih zero
2 r zero
3 r zero
4 r zero
2 ow zero
3 ow zero
4 ow zero
""".strip()
, "zero")

raw = raw.replace(
"""
2 z zero
3 z zero
4 z zero
2 iy zero
3 iy zero
4 iy zero
2 r zero
3 r zero
4 r zero
2 ow zero
3 ow zero
4 ow zero
2 sp zero
""".strip()
, "zero")

raw = raw.replace(
"""
2 z zero
3 z zero
4 z zero
2 iy zero
3 iy zero
4 iy zero
2 r zero
3 r zero
4 r zero
2 ow zero
3 ow zero
4 ow zero
""".strip()
, "zero")

raw = raw.replace(
"""
2 ow oh
3 ow oh
4 ow oh
2 sp oh
""".strip()
, "oh")

raw = raw.replace(
"""
2 ow oh
3 ow oh
4 ow oh
""".strip()
, "oh")

raw = re.sub(r'\d \S+ \S+\n', '', raw)

f = open("../output.txt", "w")
f.write(raw)
f.close()