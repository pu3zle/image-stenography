# Image Stenograpy Project

A Python Project for hiding text inside photos<br>
*\*to be expanded for more than just text\**

## ~ How it works ~

The basic concept is very well explained [here](https://www.geeksforgeeks.org/image-based-steganography-using-python/).<br>
In addition to this, this script also encrypts the text before hiding it in the photo. Thus, if someone found the text in a photo, it would be useless
without the **key** used for encryption. <br>
The text encryption method used is called [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher).<br>

## ~ Installation ~

For this to work, you will need to have [Python](https://www.python.org/downloads/) installed.<br>
Written using **Python 3.8.5**<br>

After installing the latest version of **Python**, you'll also need **Pillow**.<br>
To install it and also to initialise all the folders and files, run `init.bat`<br>

After `init.bat` is finished, you're good to go.

## ~ Using steno.py ~

`steno.py <option> [ <randomness> <filename_of_photo> ] or [ <filename_of_photo> ]`

This script has **2 main options**:
  - Encryption --> `-enc`
  - Decryption --> `-dec`

## ~ Encryption ~

*Example: `steno.py -enc 1 example.png`*

### The first argument is ***randomness***
Its value decides how the encryption key will be generated (manually/randomly).<br>
If the value is **1** -- a random key will be generated and stored inside `key.txt`.<br>
If the value is **0** -- a key needs to be manually written inside `key.txt` and will be used for encryption.<br>

### The second argument is ***filename***
This argument is the name (+extension) of the photo that will be used to store the text.<br>
The photo needs to be stored inside the folder `exhibits`.

## ~ Decryption ~

*Example: `steno.py -dec example.png`*

### The only argument is **filename**
This is the filename of the photo you want to get the data out of.<br>
It should also contain the extension of the file!<br>
The photo should be inside a folder called `results`

Before runnning this, make sure you have the correct key inside `key.txt`<br>
The decrypted message will be found in a file named `message_decrypted.txt`
