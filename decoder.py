import re
from Utils.functions import *
from pycipher import *
from colorama import Fore, Style,init


banner="""
 _____ ___________      _____                  _      _____           _ 
/  __ \_   _|  ___|    /  __ \                | |    |_   _|         | |
| /  \/ | | | |_ ______| /  \/_ __ _   _ _ __ | |_ ___ | | ___   ___ | |
| |     | | |  _|______| |   | '__| | | | '_ \| __/ _ \| |/ _ \ / _ \| |
| \__/\ | | | |        | \__/\ |  | |_| | |_) | || (_) | | (_) | (_) | |
 \____/ \_/ \_|         \____/_|   \__, | .__/ \__\___/\_/\___/ \___/|_|
                                    __/ | |                             
                                   |___/|_|                             
"""

print(Style.BRIGHT+Fore.GREEN+banner+Fore.RESET)

string = input("Enter the text : ")
key = input("Enter Key (if none press enter): ")
flag = input("Enter flag (if none press enter): ")

if flag==None:
	flag=""

ic=getIC(string)

if not key:
	if set(string).issubset({'0', '1',' '}):
		print(Fore.YELLOW+"\nPossible Binary : ",Style.BRIGHT+Fore.GREEN+bin(string)+Fore.RESET)

	if len(string)%8==0 and string[-1]=="=" and any(x not in string for x in b_32):
		print(Fore.YELLOW+"\nPossible Base32 : ",Fore.GREEN+b32(string)+Fore.RESET) 

	if len(string)%4==0 and string[-1]== '=' and len(set(string))<=65:
		print(Fore.YELLOW+"\nPossible Base64 : ",Fore.GREEN+b64(string)+Fore.RESET)

	if set(string).issubset({'-', '.','/'," "}):
		print(Fore.YELLOW+"\nPossible Morse : ",Fore.GREEN+morse(string,flag)+Fore.RESET)

	if re.search(r'[0-9a-fA-F]+',string):
		print(Fore.YELLOW+"\nPossible Hex : ",Fore.GREEN+hex(string)+Fore.RESET)

	if b85Checker(string):
		print(Fore.YELLOW+"\nPossible Base85 : ",Fore.GREEN+b85(string)+Fore.RESET)

	if re.search(r'^[1-9]+$',string):
		print(Fore.YELLOW+"\nPossible Morbit ")
		morbit(string,flag)

	if re.search(r"^[0-7\s]+$",string):
		print(Fore.YELLOW+"\nPossible Octal : ",Fore.GREEN+octal(string)+Fore.RESET)

	if set(string).issubset({">","<","+","-",".","[","]"," "}):
		print(Fore.YELLOW+"\nPossible brainfuck :",Fore.GREEN+"https://www.dcode.fr/brainfuck-language")

	if set(string).issubset({"Ook.","Ook?","Ook!"}):
		print(Fore.YELLOW+"\nPossible ook :",Fore.GREEN+"https://www.dcode.fr/ook-language")
		
	if set(string).issubset({"(","!","[","]","+",")"}):
		print(Fore.YELLOW+"\nPossible Jsfuck :",Fore.GREEN+"https://enkhee-osiris.github.io/Decoder-JSFuck/")

	if ic != None and ic[0] > 0.02:
		print(Fore.YELLOW+"\nPossible Keyboard Shift Cipher"+Fore.RESET)
		a,b,c,d = keyboard_cipher(string)
		print("Right Shift :",Fore.GREEN+''.join(a)+Fore.RESET)
		print("Left Shift  :",Fore.GREEN+''.join(b)+Fore.RESET)
		print("Up Shift    :",Fore.GREEN+''.join(c)+Fore.RESET)
		print("Down Shift  :",Fore.GREEN+''.join(d)+Fore.RESET)
		max_key = break_caesar(string)
		if flag.lower() in Caesar(max_key[1]).decipher(string).lower():
			print(Fore.YELLOW+"\nPossible Caesar Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Caesar(max_key[1]).decipher(string)+Fore.RESET,"Key:",Fore.BLUE+str(max_key[1]))
		if flag.lower() in atbash(string).lower():
			print(Fore.YELLOW+"\nPossible Atbash Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,atbash(string))
		print(Fore.YELLOW+"\nPossible Vigenere Cipher") 
		break_3(string,"v",flag)
		print(Fore.YELLOW+"\nPossible Beaufort Cipher")
		break_3(string,"b",flag)
		print(Fore.YELLOW+"\nPossible Gronsfeld Cipher")
		break_gronsfeld(string,flag)
		max_key = break_caesar(string)
		max_key = break_affine(string)
		if flag.lower() in Affine(max_key[1][0],max_key[1][1]).decipher(string).lower():
			print(Fore.YELLOW+"\nPossible Affine Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Affine(max_key[1][0],max_key[1][1]).decipher(string)+Fore.RESET,"Key:",Fore.BLUE+str(max_key))
		print(Fore.YELLOW+"\nPossible ROT Cipher\nBreaking ROT")
		for i in range(2,30):
			if flag.lower() in rotN(string,i).lower():
				print(Fore.YELLOW+"Decoded String:",Fore.GREEN+rotN(string,i)+Fore.RESET,Fore.BLUE+"Rot"+str(i))
		max_key = break_railfence(string)
		if flag.lower() in Railfence(max_key[1]).decipher(string).lower():
			print(Fore.YELLOW+"\nPossible Railfence Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Railfence(max_key[1]).decipher(string)+Fore.RESET,"Key:",Fore.BLUE+str(max_key[1]))
		print(Fore.YELLOW+"\nPossible Autokey Cipher")
		break_3(string,"a",flag)
		print(Fore.YELLOW+"\nPossible Substitution Cipher","use quipquip")
else:
	string=string.lower().replace(" ","")
	print(string)
	if len(key)==1 and key.isdigit():
		print(Fore.YELLOW+"\nPossible Caesar Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Caesar(key).decipher(string))
		print(Fore.YELLOW+"\nPossible Railfence Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Railfence(key).decipher(string))
	if key.isalpha():
		print(Fore.YELLOW+"\nPossible Vigenere Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Vigenere(key).decipher(string))
		print(Fore.YELLOW+"\nPossible Beaufort Cipher"+Fore.RESET,"Decoded String:"+Fore.GREEN,Beaufort(key).decipher(string))
	if all(isinstance(item, int) for item in key):
		print(Fore.YELLOW+"\nPossible Gronsfeld Cipher"+Fore.RESET,"Decoded String:",Gronsfeld(list(key)).decipher(string))
	if " " in key:
		key_set - key.split(" ")
		print(Fore.YELLOW+"\nPossible Affine Cipher"+Fore.RESET,"Decoded String:",Affine(key_set[0],key_set[1]).decipher(string))
	print(Fore.YELLOW+"\nPossible Autokey Cipher"+Fore.RESET,"Decoded String:",Autokey(key).decipher(string))
	if len(key)==26:
		print(Fore.YELLOW+"\nPossible Substitution Cipher"+Fore.RESET,"Decoded String:",SimpleSubstitution(key).decipher(string))
	if len(key)==25:
		print(Fore.YELLOW+"\nPossible playfair Cipher"+Fore.RESET,"Decoded String:",Playfair(key).decipher(string))
	
	#print("\nPossible Polybius Cipher","Decoded String:",Polybius(key).decipher(string))	



#nGmni Tskcxipo esdskkxgmejvc

# if ic[0] < 0.055 and ic[0] >= 0.035 :
# 		max_key = break_caesar(string)
# 		if flag in Caesar(max_key[1]).decipher(string):
# 			print("Possible Caesar Cipher","Decoded String:",Caesar(max_key[1]).decipher(string),"Key:",max_key[1])
# 		# else:
# 		# 	if mode:
# 		# 		print("Possible Caesar Cipher","Decoded String:",Caesar(max_key[1]).decipher(string),"Key:",max_key[1])
# 		print("Possible Vigenere Cipher") 
# 		break_3(string,"v",flag)
# 		print("Possible Beaufort Cipher")
# 		break_3(string,"b",flag)
# 		print("Possible Gronsfeld Cipher")
# 		break_gronsfeld(string,flag)
# 	elif ic[0]>=0.06:
# 		max_key = break_caesar(string)
# 		if flag in Caesar(max_key[1]).decipher(string):
# 			print("Possible Caesar Cipher","Decoded String:",Caesar(max_key[1]).decipher(string),"Key:",max_key[1])
# 		max_key = break_affine(string)
# 		if flag in Affine(max_key[1][0],max_key[1][1]).decipher(string):
# 			print("Possible Affine Cipher","Decoded String:",Affine(max_key[1][0],max_key[1][1]).decipher(string),"Key:",max_key)
# 	print("Possible ROT Cipher\nBreaking ROT")
# 	for i in range(2,30):
# 		if flag in rotN(string,i):
# 			print("Decoded String:",rotN(string,i),"Rot"+str(i))