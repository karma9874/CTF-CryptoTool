# CTF-CryptoTool
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) 
[![Twitter Follow](https://img.shields.io/twitter/follow/karma9874?label=Follow&style=social)](https://twitter.com/karma9874)
[![GitHub followers](https://img.shields.io/github/followers/karma9874?label=Follow&style=social)](https://github.com/karma9874)

CTF-CryptoTool is a tool written in python, for breaking crypto text of CTF challenges. It tries to decode the cipher by bruteforcing it with all known cipher decoding methods easily. Also works for the cipher which does not have a key.

| Known Ciphers  | Known Encodings | Known Obfuscator |
| ------------- |:-------------:| :-----:|
| Affine Cipher | Base64 | Brainfuck |
| Ceaser Cipher      | Base32      |   JSFuck |
| Vigenere Cipher | Base85      |     Ook |
| Autokey Cipher | Binary      |    
|Atbash Cipher | Octal      |    
| Gronsfeld Cipher | Hex      |     
| Railfence Cipher | Morse      |     
| Keyboard Shift | Rot      |     
| Morbit Cipher| Base58 |

## Screenshots
![CTF-CryptoTool](https://github.com/karma9874/CTF-CryptoTool/blob/master/Screenshots/1.PNG)

## Installation
This tool will run on python3
``` 
git clone https://github.com/karma9874/CTF-CryptoTool.git
cd CTF-CryptoTool 
pip3 install -r requirments.txt
  ```

## Usage 
` Just throw the cipher to it `
``` 
python3 decoder.py 
Enter the text  : Feed the cipher text
Enter Key       : Enter key if you know any (optional)
Enter flag 	    : Enter some letters of the flag if you know (optional)
				Eg: While playing picoCTF you can enter the flag as picoCTF so it can match that text with the ouputs otherwise you may get much more bogus strings   	
```

## Reference
[python_cryptanalysis](https://github.com/jameslyons/python_cryptanalysis)