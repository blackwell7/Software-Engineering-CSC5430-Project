'''This module checks a given email id is valid or not
and returns the status'''
import re

def IsValidEmail(email): # this is the method where the email entered by the user is passed as the parameter for verification
    emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+       #  for Username we are checking and limiting the alphabets from a-z and A - Z
    @                       # For making sure that there is an @ because there is no mail without @
    [a-zA-Z0-9.-]+          # Domain Name like gmail.com
    (\.[a-zA-Z]{2,4})       # dot-something
    )''', re.VERBOSE)

    email_address = emailRegex.findall(email)
    if len(email_address) != 0:
        return True# if mail exist the length is not zero definitely.
    else:
        return False