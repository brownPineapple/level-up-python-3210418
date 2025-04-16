from random import randint

def generate_password(word_count):
  passphrase = ''
  with open ('diceware_wordlist.txt' , 'r+') as wordlist:
    words = wordlist.readlines()
    for i in range(0,word_count):
      word = randint(0, len(words))
      passphrase = passphrase + ' ' + words[i]
  print(passphrase)