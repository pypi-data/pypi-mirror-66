# equation_cipher

The encryption algorithm which uses two steps encryption.

This algorithm will be a half way decryptable algorithm; i.e. To get its
decryption you will need to encrypt it partially and decrypt it partially to
check if the encrypted form of the text is right form or not.

# Features

Uses one way encryption and half way decryption.

Creates different and unique encryption of the same target string every millisecond.

Can be partially decrypted.


# Usage

```
$ pip install equation-cipher
``` 

```
import datetime
from cipher.equation_cipher import Encrypter
from cipher.equation_decipher import Decrypter

target = 'hello@123'
encrypter_obj = Encrypter()

encrypted_target = encrypter_obj.encrypt(target)
print("encrypted string", encrypted_target)

# here datetime object is required, since the algorithm uses date as well as time.
encryption_by_date = encrypter_obj.encrypt_by_date(target, datetime.datetime.now())
print("Encrypted by date:", encryption_by_date)

# decryption
decrypter_obj = Decrypter()
decrypted_text_check = decrypter_obj.match_decrypt('hello@123', encrypted_target)
if encrypted_text_check:
    print("The passed string matches the passed encrypted pattern.")
else:
    print("The passed string does not match the passed encrypted pattern.")
```
