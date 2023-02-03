import base64
from collections import Counter

from set1.c2 import xor


FILES = [base64.b64decode(b) for b in open("19-enc.txt").readlines()]




def try_letter(pos, letter_to_try, all_decoded):
    ctr = Counter([
        xor(letter_to_try, i) for i in FILES
    ])
    best_key = sorted(ctr.items(), key=lambda x: x[1], reverse=True)[-1][0]
    return [xor(best_key, i) for i in FILES]

def try_letters(letters):
    if isinstance(letters, str):
        letters = letters.encode("utf-8")
    ctr = Counter([
        xor(letters, i) for i in FILES
    ])
    best_key = sorted(ctr.items(), key=lambda x: x[1], reverse=True)[-1][0]
    return [xor(best_key, i) for i in FILES]

# Key so far
#  b'\xbcL'
# b'\xbcL\xd7\xbf'
# b'\xbcL\xd7\xbfE\x83\xc9\x91'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed\xa7\x0e'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed\xa7\x0e\xe20R\xa8'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed\xa7\x0e\xe20R\xa8D\x9f'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed\xa7\x0e\xe20R\xa8D\x9fV2\xbc\xcb&'
# b'\xbcL\xd7\xbfE\x83\xc9\x91\xc5t\x162\x19\xbd\xf2\xf9\x9b\xfd\xff\xb7\xb6z\xed\xa7\x0e\xe20R\xa8D\x9fV2\xbc\xcb&\x81\x1e'
'''
I have met them at close of day
Coming with vivid faces
From counter or desk among grey
Eighteenth-century houses.
I have passed with a nod of the head
Or polite meaningless words,
Or have lingered awhile and said
Polite meaningless words,
And thought before I had done
Of a mocking tale or a gibe
To please a companion
Around the fire at the club,
Being certain that they and I
But lived where motley is worn:
All changed, changed utterly:
A terrible beauty is born.
That woman's days were spent
In ignorant good will,
Her nights in argument
Until her voice grew shrill.
What voice more sweet than hers
When young and beautiful,
She rode to harriers?
This man had kept a school
And rode our winged horse.
This other his helper and friend
Was coming into his force;
He might have won fame in the end,
So sensitive his nature seemed,
So daring and sweet his thought.
This other man I had dreamed
A drunken, vain-glorious lout.
He had done most bitter wrong
To some who are near my heart,
Yet I number him in the song;
He, too, has resigned his part
In the casual comedy;
He, too, has been changed in his turn.
Transformed utterly:
A terrible beauty is born.
'''


# Code Ran
"""
try_letter(0, b"A", None)
try_letter(0, b"S", None)
try_letter(0, b"T", None)
clear
try_letter(0, b"T", None)
try_letter(0, b"E", None)
try_letter(0, b"D", None)
try_letter(0, b"T", None)
try_letter(1, b"h", None)
clear
import strings
import string
clear
string.ascii_uppercase
[try_letter(0,i,None) for i in  string.ascii_uppercase]
[try_letter(0,i.encode('utf-8'),None) for i in  string.ascii_uppercase]
res = [all(try_letter(0,i.encode('utf-8'),None)) for i in  string.ascii_uppercase]
res
out = [try_letter(0,i.encode('utf-8'),None) for i in  string.ascii_uppercase]
[all(x.isalpha() for x in i) for i in out]
try_letter(0, "Y",None)
try_letter(0, b"Y",None)

def try_letters(letters):
    if isinstance(letters, str):
        letters = letters.encode("utf-8")
    ctr = Counter([
        xor(letters, i) for i in FILES
    ])
    best_key = sorted(ctr.items(), key=lambda x: x[1], reverse=True)[-1][0]
    return [xor(best_key, i) for i in FILES]
FILES[0]
xor(FILES[0], b"You")
k = xor(FILES[0], b"You")
 [xor(k, i) for i in FILES]
k = xor(FILES[0], b"I ")
 [xor(k, i) for i in FILES]
k
k = xor(FILES[2], b"From")
 [xor(k, i) for i in FILES]
k
k = xor(FILES[1], b"Coming")
 [xor(k, i) for i in FILES]
k = xor(FILES[1], b"Coming ")
 [xor(k, i) for i in FILES]
k = xor(FILES[3], b"Eighteen ")
 [xor(k, i) for i in FILES]
k
k = b'\xbcL\xd7\xbfE\x83\xc9\x91'
 [xor(k, i) for i in FILES]
k = xor(FILES[-1], b"A terrible")
 [xor(k, i) for i in FILES]
k
k = xor(FILES[-2], b"Transformed")
 [xor(k, i) for i in FILES]
 [i, xor(k, i) for i in enumerate(FILES)]
 [idx, xor(k, i) for i, idx in enumerate(FILES)]
 [(idx, xor(k, i)) for i, idx in enumerate(FILES)]
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[34], b"Yet I number")
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[3], b"Eighteenghth-century")
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[34], b"Yet I number")
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)][:10]
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)][:15]
k = xor(FILES[12], b"Being certain")
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[7], b'Polite meaning")
k = xor(FILES[7], b'Polite meaning')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k
max(len(i) for i in FILES)
len(k)
clear
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[5], b'Or polite meaning')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k = xor(FILES[4], b'I have passed with')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k
k = xor(FILES[5],  b'Or polite meaningless')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
len(k)
k
k = xor(FILES[6], b'Or have lingered awhile')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
k
k = xor(FILES[37], b'He, too, has been changed')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES)]
len(k)
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES)]
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) > len(k)]
k
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k = xor(FILES[20] b'What voice more sweet than ')
k = xor(FILES[20], b'What voice more sweet than ')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k = xor(FILES[27], b'He might have won fame in the')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k
k = xor(FILES[4], b'I have passed with a nod of the')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
len(k)
k
clear
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k = xor(FILES[37], b'He, too, has been changed in his')
 [(idx, xor(k, i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
len(k)
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
len(k)
k = xor(FILES[37], b'He, too, has been changed in his ')
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
len(k)
k = xor(FILES[4], b'I have passed with a nod of the h')
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k = xor(FILES[4], b'I have passed with a nod of the head')
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
len(k)
k
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k = xor(FILES[37], b'He, too, has been changed in his turn.')
 [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES) if len(i) >= len(k)]
k
clear
f =  [(idx, xor(k, i), len(i)) for idx, i in enumerate(FILES)]
f
out = [i[1] for i in f]
out
print(out)
print(out)
out
_ = [print(i.decode()) for i in out]
"""