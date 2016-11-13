# Neural cryptography protocol for exchange key

Implementation of the exchange key protocol described in International Journal of Advanced Research in
Computer Science and Software Engineering.

Neural crypto avoids a Diffie-Hellman exchange key protocol from MITM attack.

## Generate key
```bash
run.py -K <nb hidden neurons> -N <nb input neurons> -L <range of weight> -key <key options>
```
key length options : 128, 192, 256


## use with openSSL
```bash
openssl enc -aes128 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes192 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
openssl enc -aes256 -K <key> -iv <init vector> -in <inputfile> -out <outputfile>
```