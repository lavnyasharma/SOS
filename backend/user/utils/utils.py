from ..models import user
def is_user(num):
    return user.objects.filter(phone_number=num).exists()