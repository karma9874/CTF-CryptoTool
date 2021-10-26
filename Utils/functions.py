from itertools import permutations
import base64
import base58
from Utils.base91 import b91decode, b91check
import binascii
import numpy as np
import re
from Utils.ngram_score import ngram_score
from pycipher import *
from tqdm import tqdm
import collections
from colorama import Fore, Style,init

qgram = ngram_score('Utils/quadgrams.txt')
trigram = ngram_score('Utils/trigrams.txt')

class nbest(object):
    def __init__(self,N=1000):
        self.store = []
        self.N = N
        
    def add(self,item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]
    
    def __getitem__(self,k):
        return self.store[k]

    def __len__(self):
        return len(self.store)

def b64(s):
    try:
        return base64.b64decode(s).decode("utf-8")
    except:
        return 0
        
def b32(s):
    try:
        return base64.b32decode(s).decode("utf-8")
    except:
        return 0

def b58(s):
	try:
		return base58.b58decode(s).decode("utf-8")
	except:
		return 0
	
def b85(s):
    try:
        return base64.a85decode(s).decode("utf-8")
    except:
        return 0

def b91(s):
    try:
        return b91decode(s)
    except:
        return 0

def hex(s):
    try:
        return binascii.unhexlify(s).decode('utf-8')  
    except:
        return 0

def bin(s):
    char=""
    for b in s.split(" "):
        try:
            char+= chr(int(b, 2))
        except:
            pass
    return char


def b85Checker(s):
    for i in s:
        if ord(i) not in range(33,117):
            return False
    return True


b_32=["0","1","8","9"]
MORSE_CODE_DICT = {'..-': 'U', '--..--': ', ', '....-': '4', '.....': '5', '-...': 'B', '-..-': 'X', '.-.': 'R', '--.-': 'Q', '--..': 'Z', '.--': 'W', '-..-.': '/', '..---': '2', '.-': 'A', '..': 'I', '-.-.': 'C', '..-.': 'F', '---': 'O', '-.--': 'Y', '-': 'T', '.': 'E', '.-..': 'L', '...': 'S', '-.--.-': ')', '..--..': '?', '.----': '1', '-----': '0', '-.-': 'K', '-..': 'D', '----.': '9', '-....': '6', '.---': 'J', '.--.': 'P', '.-.-.-': '.', '-.--.': '(', '--': 'M', '-.': 'N', '....': 'H', '---..': '8', '...-': 'V', '--...': '7', '--.': 'G', '...--': '3', '-....-': '-', '\n' : ' '}
MORBIT = ['..', '.-', '. ', '-.', '--', '- ', ' .', ' -', '  ']
lookup_table = {'A' : 'Z', 'B' : 'Y', 'C' : 'X', 'D' : 'W', 'E' : 'V','F' : 'U', 'G' : 'T', 'H' : 'S', 'I' : 'R', 'J' : 'Q', 'K' : 'P', 'L' : 'O', 'M' : 'N', 'N' : 'M', 'O' : 'L', 'P' : 'K', 'Q' : 'J', 'R' : 'I', 'S' : 'H', 'T' : 'G', 'U' : 'F', 'V' : 'E', 'W' : 'D', 'X' : 'C', 'Y' : 'B', 'Z' : 'A'} 

def morse(ciphertxt,flag=None): 
    plaintxt = ''
    for word in ciphertxt.strip().split("  "):
        for c in word.strip().split(" "):
            if c in MORSE_CODE_DICT:
                plaintxt += MORSE_CODE_DICT[c]
            else:
                pass
        plaintxt += ' '
    return plaintxt
    #print(Fore.GREEN+plaintxt+Fore.RESET)


def pretty_print(header,data):
    print(Fore.YELLOW+"\n"+header+" : ",Style.BRIGHT+Fore.GREEN+data+Fore.RESET)

def morbit(ciphertxt,flag=None):
    if flag==None:
        flag=""
    scores=[]
    for p in permutations('123456789'):
        MORBIT_CODE_DICT = dict(zip(p, MORBIT))
        morsetxt = ""
        for c in ciphertxt:
            if c in MORBIT_CODE_DICT:
                morsetxt += MORBIT_CODE_DICT[c]
        if flag in morse(morsetxt,flag):
            print(Fore.GREEN+morse(morsetxt,flag)+Fore.RESET)
        #scores.append((qgram.score(morse1(morsetxt,flag)),p,morse1(morsetxt,flag)))
    #s = sorted(scores,reverse=True)
    

def octal(octal_str):
    str_converted = ""
    for octal_char in octal_str.strip().split(" "):
        try:
            str_converted += chr(int(octal_char, 8))
        except:
            return 0
    return str_converted

def atbash(message):
    return Atbash().decipher(message)

def getIC(s):
    s="".join( [x.upper() for x in s.split() if  x.isalpha()])
    N = len(s)
    if N ==0: return
    freqs = collections.Counter(s)
    alphabet = map(chr, range( ord('A'), ord('Z')+1))
    freqsum = 0.0
    for letter in alphabet:
        freqsum += freqs[ letter ] * ( freqs[ letter ] - 1 )
    IC = freqsum / ( N*(N-1) )
    return (IC,N)

def keyboard_cipher(s):
    s=s.lower()
    keyboard = np.array(        [
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=' ],
                    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']' ],
                    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '\\' ],
                    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '-', '='],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=' ],
                    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '-', '=']
                   ]
                    )
    l=[]
    r=[]
    u=[]
    d=[]
    for i in s:
        if i != " ":
            solutions = np.argwhere(keyboard == i)
            r.append(keyboard[solutions[0][0],solutions[0][1]+1])
            l.append(keyboard[solutions[0][0],solutions[0][1]-1])
            u.append(keyboard[solutions[0][0]-1,solutions[0][1]])
            d.append(keyboard[solutions[0][0]+1,solutions[0][1]])
        else:
            r.append(" ")
            l.append(" ")
            u.append(" ")
            d.append(" ")
    return l,r,u,d    

def rotN(s,i):
    abc = "abcdefghijklmnopqrstuvwxyz"
    return "".join([abc[(abc.find(c)+i)%26] for c in s])

def break_caesar(s):
    s = re.sub('[^A-Z]','',s.upper())
    scores = []
    for i in range(26):
        scores.append((qgram.score(Caesar(i).decipher(s)),i))
    return max(scores)

def break_affine(s):
    s = re.sub('[^A-Z]','',s.upper())
    scores = []
    for i in [1,3,5,7,9,11,15,17,19,21,23,25]:
        scores.extend([(qgram.score(Affine(i,j).decipher(s)),(i,j)) for j in range(0,25)])
    return max(scores)

def break_railfence(ctext):
    ctext = re.sub('[^A-Z]','',ctext.upper())
    print(ctext)
    scores = []
    for i in range(2,50):
        scores.append((qgram.score(Railfence(i).decipher(ctext)),i))
    return max(scores)

def break_3(ctext,cipher=None,Flag=None):
    if Flag==None:
        Flag=""
    if cipher == "b":
        print(Fore.YELLOW+"Breaking Beaufort Cipher"+Fore.RESET)
    if cipher == "a":
        print(Fore.YELLOW+"Breaking AutoKey Cipher"+Fore.RESET)
    if cipher == "v":
        print(Fore.YELLOW+"Breaking Vigenere Cipher"+Fore.RESET)
    #print("This may take a while\n")
    N=100
    ctext = re.sub(r'[^A-Z]','',ctext.upper())
    for KLEN in range(3,17):
        rec = nbest(N)
        for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ',3):
            key = ''.join(i) + 'A'*(KLEN-len(i))
            if cipher=='b':
                pt = Beaufort(key).decipher(ctext)
            elif cipher=='a':
                pt = Autokey(key).decipher(ctext)
            elif cipher=='v':
                pt = Vigenere(key).decipher(ctext)
            score = 0
            for j in range(0,len(ctext),KLEN):
                score += trigram.score(pt[j:j+3])
            rec.add((score,''.join(i),pt[:30]))
        next_rec = nbest(N)
        for i in range(0,KLEN-3):
            for k in range(N):
                for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    key = rec[k][1] + c
                    fullkey = key + 'A'*(KLEN-len(key))
                    if cipher=='b':
                        pt = Beaufort(fullkey).decipher(ctext)
                    elif cipher=='a':
                        pt = Autokey(fullkey).decipher(ctext)
                    elif cipher=='v':
                        pt = Vigenere(fullkey).decipher(ctext)
                    score = 0
                    for j in range(0,len(ctext),KLEN):
                        score += qgram.score(pt[j:j+len(key)])
                    next_rec.add((score,key,pt[:30]))
            rec = next_rec
            next_rec = nbest(N)
        bestkey = rec[0][1]
        if cipher=='b':
            pt = Beaufort(bestkey).decipher(ctext)
        elif cipher=='a':
            pt = Autokey(bestkey).decipher(ctext)
        elif cipher=='v':
            pt = Vigenere(bestkey).decipher(ctext)
        bestscore = qgram.score(pt)
        for i in range(N):
            if cipher=='b':
                pt = Beaufort(rec[i][1]).decipher(ctext)
            elif cipher=='a':
                pt = Autokey(rec[i][1]).decipher(ctext)
            elif cipher=='v':
                pt = Vigenere(rec[i][1]).decipher(ctext)
            score = qgram.score(pt)
            if score > bestscore:
                bestkey = rec[i][1]
                bestscore = score
        if cipher=='b':
            if Flag in Beaufort(bestkey).decipher(ctext):
                print("Decoded String",Fore.GREEN+Beaufort(bestkey).decipher(ctext)+Fore.RESET,'Key: '+Fore.BLUE+bestkey+Fore.RESET)
        elif cipher=='a':
            if Flag in Autokey(bestkey).decipher(ctext):
                print("Decoded String",Fore.GREEN+Autokey(bestkey).decipher(ctext)+Fore.RESET,'Key: '+Fore.BLUE+bestkey+Fore.RESET)
        elif cipher=='v':
            if Flag in Vigenere(bestkey).decipher(ctext):
                print("Decoded String",Fore.GREEN+Vigenere(bestkey).decipher(ctext)+Fore.RESET,'Key: '+Fore.BLUE+bestkey+Fore.RESET)

def break_gronsfeld(ctext,Flag=None):
    if Flag == None:
        Flag=""
    print(Fore.YELLOW+"Breaking Gronsfeld Cipher"+Fore.RESET)
    #print("This may take a while\n")
    ctext = re.sub(r'[^A-Z]','',ctext.upper())
    N=100
    for KLEN in range(3,17):
        rec = nbest(N)
        for i in permutations('0123456789',3):
            key = ''.join(i) + '0'*(KLEN-len(i))
            key = [int(i) for i in list(key)]
            pt = Gronsfeld(list(key)).decipher(ctext)
            score = 0
            for j in range(0,len(ctext),KLEN):
                score += trigram.score(pt[j:j+3])
            rec.add((score,''.join(i),pt[:30]))

        next_rec = nbest(N)
        for i in range(0,KLEN-3):
            for k in range(N):
                for c in '0123456789':
                    key = rec[k][1] + c
                    fullkey = key + '0'*(KLEN-len(key))
                    fullkey = [int(i) for i in list(fullkey)]
                    pt = Gronsfeld(list(fullkey)).decipher(ctext)
                    score = 0
                    for j in range(0,len(ctext),KLEN):
                        score += qgram.score(pt[j:j+len(key)])
                    next_rec.add((score,key,pt[:30]))
            rec = next_rec
            next_rec = nbest(N)
        bestkey = rec[0][1]
        bestkey = [int(i) for i in list(bestkey)]
        pt = Gronsfeld(list(bestkey)).decipher(ctext)
        bestscore = qgram.score(pt)
        for i in range(N):
            scam = list(rec[i][1])
            scam = [int(i) for i in scam]
            pt = Gronsfeld(scam).decipher(ctext)
            score = qgram.score(pt)
            if score > bestscore:
                bestkey = scam
                bestscore = score   
        if Flag in Gronsfeld(bestkey).decipher(ctext):
            print("Decoded String",Fore.GREEN+Gronsfeld(bestkey).decipher(ctext)+Fore.RESET,'Key: ['+Fore.BLUE+''.join(str(x) for x in bestkey)+Fore.RESET+']')
