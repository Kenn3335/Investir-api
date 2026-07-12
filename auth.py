from passlib.context import CryptContext
import random
import string


# =====================
# PASSWORD SECURITY
# =====================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):

    return pwd_context.hash(password)



def verify_password(password, hashed_password):

    return pwd_context.verify(
        password,
        hashed_password
    )



# =====================
# REFERRAL CODE
# =====================

def generate_referral_code():

    letters = string.ascii_uppercase

    numbers = string.digits

    code = (
        ''.join(random.choice(letters) for _ in range(4))
        +
        ''.join(random.choice(numbers) for _ in range(4))
    )

    return code
