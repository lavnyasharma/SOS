from cv001.exceptions import invalidinput
from cv001.utils.uid import decode_id
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..models import *
from .uid import *
import re

def savephone(phone, uid):
    if re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', phone):
        payload = decode_id(uid)
        phid = encode_id(p=payload['p'], t='ph', cd=str(timezone.now()))
        instance = PhoneNumber.objects.create(
            PHID=phid, UID=uid, phone_number=phone)
        instance.save()
        return instance
    raise invalidinput()
    


def savepin(pin, uid):
    if re.match(r'^[1-9][0-9]{5}$',pin):
        payload = decode_id(uid)
        pcid = encode_id(p=payload['p'], t='pc', cd=str(timezone.now()))
        instance = Pincode.objects.create(
            PCID=pcid, UID=uid, pincode_number=pin)
        instance.save()
        return instance
    raise invalidinput()



def update_phone(PHID, phone):
    phone_instance = PhoneNumber.objects.get(PHID=PHID)
    phone_instance.phone_number = phone
    phone_instance.save()
    return phone_instance


def update_pin(PCID, pincode):
    pincode_instance = Pincode.objects.get(PCID=PCID)
    pincode_instance.pincode_number = pincode
    pincode_instance.save()
    return pincode_instance


def update_address(instance, querry_data):
    if 'addr1' in querry_data:
        instance.address_line_one = querry_data['addr1']
    if 'addr2' in querry_data:
        instance.address_line_two = querry_data['addr2']
    if 'addr3' in querry_data:
        instance.address_line_three = querry_data['addr3']
    if 'addr4' in querry_data:
        instance.address_line_four = querry_data['addr4']
    if 'district' in querry_data:
        instance.district = querry_data['district']
    if 'state' in querry_data:
        instance.state = querry_data['state']
    if 'is_home' in querry_data:
        instance.is_home = querry_data['is_home']
    if 'phone' in querry_data:
        update_phone(PHID=instance.PHID, phone=querry_data['phone'])
    if 'pincode' in querry_data:
        update_pin(PCID=instance.PCID, pincode=querry_data['pincode'])
    instance.save()
    return instance
