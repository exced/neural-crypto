# Neural cryptography protocol for exchange key

Implementation of the exchange key protocol described in International Journal of Advanced Research in
Computer Science and Software Engineering.

Neural crypto avoids a Diffie-Hellman exchange key protocol from MITM attack.

## openSSL
Required openSSL to encyrpt with AES cipher.

## Generate key and IV for AES encryption
```bash
python run.py -i <input file> -o <output file> -K <nb hidden neurons> -N <nb input neurons> -L <range of weight> -k <key length> -v <iv length>
```
key length options : 128, 192, 256
iv length : [0:256]
if inputfile is read, aes encryption is executed.

## Use with openSSL
### Cipher
```bash
openssl enc -aes128 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes192 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes256 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
```
### Decipher
```bash
openssl enc -aes128 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
openssl enc -aes192 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
openssl enc -aes256 -K <key> -iv <init vector> -in <inputfile(enc)> -out <outputfile> -d
```
