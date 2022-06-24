import secrets
import string
allowed_chars = string.ascii_letters + string.digits + string.printable
pswd = ''.join(secrets.choice(allowed_chars) for i in range(11))
print("The generated password is: rpX/HxKR*6t\n",pswd)
