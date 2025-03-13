import random
import string

def generate_password(length=12):
    """Tạo mật khẩu ngẫu nhiên."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


