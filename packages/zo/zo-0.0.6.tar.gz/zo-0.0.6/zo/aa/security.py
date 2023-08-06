from password_strength import PasswordPolicy
from password_strength import PasswordStats


def is_strong_password(password: str):
    _policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=2,  # need min. 2 uppercase letters
        numbers=2,  # need min. 2 digits
        special=2,  # need min. 2 special characters
        nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
    )
    return False if _policy.test(password) else True


def g_password_strength(password: str):
    # 0.66 will be a very good indication of a good password.
    # need a password that scores at least 0.5 with its strength
    return PasswordStats(password).strength()


# policy = PasswordPolicy.from_names(
#     strength=0.66  # need a password that scores at least 0.5 with its strength
# )
#
# print(policy.test('V3ryG00dPassw0rd?!'))
# # -> []  -- empty list means a good password


from passlib.context import CryptContext


def hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)
