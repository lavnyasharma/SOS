from user.utils.token import Token


def Gslug(model = None,user=None):
    try:
        token = Token()
        while 1:
            if model.objects.filter(slug=token).exists():
                token  = Token()
            else:
                return token
    except Exception as e:
        print(e)
        raise Exception("something went wrong")