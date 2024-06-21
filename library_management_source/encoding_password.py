import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
# print("Hashed Password:", hashed_password)

# # Check if a password matches the hashed password
# entered_password = "example_password"
# if check_password(entered_password, hashed_password):
#     print("Password matches!")
# else:
#     print("Password does not match!")
