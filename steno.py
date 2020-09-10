from PIL import Image
import string as STR
import random
import sys
import os

printables = STR.ascii_letters + STR.digits + STR.punctuation + ' ' + '\n'

def iCase(string):
    return string.lower()

def GetArgument(mode, Atype):
    if(iCase(mode) == 'enc'):
        if(iCase(Atype) == 'option'):
            return sys.argv[1]

        if(iCase(Atype) == 'randomness'):
            return sys.argv[2]
        
        if(iCase(Atype) == 'filename'):
            return sys.argv[3]
        
        return -1
    else:
        if iCase(Atype) == 'filename':
            return sys.argv[2]
        return -1

def GetBinaryList(number):
    x = [int(i) for i in bin(number)[2:]]
    if(len(x) < 8):
        while(len(x) < 8):
            x.insert(0,0)
    return x

def GetCharacterFromList(li):
    li = [str(i) for i in li]
    return (chr(int(''.join(li), 2)))
    

def helpMenu():
    return r'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                HELP MENU
                                            
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

steno.py <option> [ <randomness> <filename_of_photo> ] or [ <filename_of_photo> ]

Important notes before using the script:

The message to be encrypted must be stored inside a file named "message_to_encrypt.txt"
The photos to be used to hide the text must be stored inside a folder named "exhibits"
The manual key to be used to encrypt the message must be stored inside a file names "key.txt"
(If instead you select <randomness> = 1, ergo choosing a random key, the file will be created automatically)

RUN: steno.py init
To create all the required files and folders automatically

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are only 2 choices for <option>:
    -dec   --> decrypt
    -enc   --> encrypt

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                ENCRYPTION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The former argument is <randomness>
If you choose is to be 1, a random key will be generated in "key.txt" and used to encrypt your message
If you choose is to be 0, it is expected that you have key written inside a file named "key.txt". You get an
error if not

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The latter argument is the filename of the photo you choose to hide the data into
It should also contain the extension of the file!
The photo should be inside a folder called "exhibits"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                DECRYPTION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only argument is the filename of the photo you want to get the data out of
It should also contain the extension of the file!
The photo should be inside a folder called "results"

The decrypted message will be found in a file named "message_decrypted.txt"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    '''

def GetImage(mode, string):
    if(iCase(mode) == 'enc'):
        return ".\\exhibits\\" + string 
    return '.\\results\\' + string

def StripExtension(filename):
    index = filename.find('.')
    return filename[:index]

def SaveKey(KEY):
    with open('key.txt', 'w') as file:
        file.write(KEY)

def GetKey():
    try:
        with open('key.txt', 'r') as file:
            key = file.readlines()
            if(key):
                return key
            return -1
    except:
        return -1

def GetMessage():
    try:
        with open ('message_to_encrypt.txt', 'r') as file:
            message = file.readlines()
            if(message):
                return message
            return -1
    except:
        return -1

def SaveMessage(message):
    with open("message_decrypted.txt", 'w') as file:
        file.write(message)

def GetRandomKey():
    size = random.randint(13, 37)

    key = []

    for i in range(size):
        key.append(printables[random.randint(0, len(printables) - 1)])

    return(''.join(key))

def EncryptText(key, text):
    key_length = len(key)
    message = list(text)
    
    for i, value in enumerate(message):
        key_index = i % key_length
        new_char = printables[(printables.find(key[key_index]) + printables.find(value)) % len(printables)]
        message[i] = new_char
    
    return message

def DecryptText(key, text):
    key = ''.join(key)
    key_length = len(key)
    for i, value in enumerate(text):
        key_index = i % key_length
        new_char = printables[(printables.find(value) - printables.find(key[key_index])) % len(printables)]
        text[i] = new_char
    
    return text

def EncryptImage():
    if(len(sys.argv) < 2 or len(sys.argv) > 4):
        print("Invalid number of arguments")
        return -1

    KEY = ''

    if(int(GetArgument('enc', 'randomness')) == 1):
        KEY = GetRandomKey()

    elif (int(GetArgument('enc', 'randomness')) == 0):
        KEY = GetKey()
        if(KEY == -1):
            return -1
        KEY = ''.join(KEY)
    else:
        print('Invalid <randomness>')
        return -1

    SaveKey(KEY)
    message = GetMessage()
    if(message == -1):
        return -1
    message = ''.join(message)

    encrypted_text = EncryptText(KEY, message)
    filename = GetArgument('enc', 'filename')
    return AddTextToImage(encrypted_text, filename)

def CreateDirectory(name):
    try:
        os.mkdir(name)
    except:
        pass

def CreateFile(name):
    with open (name, 'w') as file:
        pass

def AddTextToImage(text, filename):
    try:
        img = Image.open(GetImage('enc', filename))
    except:
        return -1
    CreateDirectory('results')

    message = [ord(i) for i in text]  

    bits = []
    for number in message:
        bits = bits + GetBinaryList(number) + [0]
    bits[-1] = 1

    index = 0
    for x in range(img.width):
        for y in range(img.height):
            if index < len(bits):
                pixel = list(img.getpixel((x,y)))
               
                for i in range(3):
                    if (pixel[i] % 2 == 0 and bits[index] == 1):
                        pixel[i] = pixel[i] + 1

                    elif(pixel[i] % 2 == 1 and bits[index] == 0):
                        pixel[i] += 1

                    index += 1
                
                img.putpixel((x,y), tuple(pixel))
                
            else:
                newimg = img.copy()
                newimg.save('.\\results\\' + StripExtension(filename) + '.png')
                return 0

def GetBitsOutOfImage(filename):
    try:
        img = Image.open(GetImage('dec', filename))
    except:
        return -1
    bits = []

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x,y))
            for i in range(3):
                bits.append(pixel[i] % 2)
            if len(bits) % 9 == 0 and pixel[2] % 2 == 1:
                return bits

def DecryptImage():
    KEY = GetKey()
    if(KEY == -1):
        return -1
    filename = GetArgument('dec', 'filename')

    bits = GetBitsOutOfImage(filename)

    if(bits == -1):
        return -1 
    chars = []

    while bits:
        chars.append(GetCharacterFromList(bits[:8]))
        bits = bits[9:]
    
    message = ''.join(DecryptText(KEY, chars))
    SaveMessage(message)
    return 0

def init():
    CreateDirectory('exhibits')
    CreateDirectory('results')
    CreateFile('key.txt')
    CreateFile('message_to_encrypt.txt')

def main():
    if(sys.argv[1] == 'init'):
        init()
        return 0

    if (len(sys.argv)) < 2 or ((sys.argv[1] != '-dec') and (sys.argv[1] != '-enc')):
        print(helpMenu())
        return 1

    exit_code = 0

    if(sys.argv[1] == '-enc'):
        exit_code = EncryptImage()
    
    else:
        exit_code = DecryptImage()
   
    if(exit_code == 0):
        print("Successful!")
    else:
        print("Failed!")

main()