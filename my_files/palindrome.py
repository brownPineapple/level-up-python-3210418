def is_palindrome(string1):
  string1 = ''.join(e for e in string1 if e.isalnum()).lower() #Remove special characters and white spaces
  string2 = string1[::-1] #Reverse the string
#  print(f'String1 - {string1} and reversed looks like - {string2}') #Uncomment to see behind the scenes
  return True if string1 == string2 else False

print("*"*8 + " Palindrome checker! " + "*"*8) #Banner 
user_string = input("Enter a string: ") #Get a string from user

print(f'Is this a Palindrome: {is_palindrome(user_string)}')