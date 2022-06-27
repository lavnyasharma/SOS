def statusgen(day, model):
    try:
        val = False
        if day == 0:
            if model.monday == True:
                val = True
        elif day == 1:
            if model.tuesday == True:
                val = True
        elif day == 2:
            if model.wednesday == True:
                val = True
        elif day == 3:
            if model.thursday == True:
                val = True
        elif day == 4:
            if model.friday == True:
                val = True
        elif day == 5:
            if model.saturday == True:
                val = True
        elif day == 6:
            if model.sunday == True:
                val = True
        return val
    except Exception as e:
        raise e


def check__avail(timing):
    return True


def slot_ava(timing):
    return 10


def convert12(str):
    txt = ""
    h1 = ord(str[0]) - ord('0')
    h2 = ord(str[1]) - ord('0')

    hh = h1 * 10 + h2

    # Finding out the Meridien of time
    # ie. AM or PM
    Meridien = ""
    if (hh < 12):
        Meridien = "AM"
    else:
        Meridien = "PM"

    hh %= 12

    # Handle 00 and 12 case separately
    if (hh == 0):
        print("12", end="")

        # Printing minutes and seconds
        for i in range(2, 8):
            print(str[i], end="")

    else:
        print(hh, end="")

        # Printing minutes and seconds
        for i in range(2, 8):
            print(str[i], end="")

    print(" " + Meridien)
