import requests
import json


def send_fmc_sms(token, msg):

    serverToken = 'AAAAgs81yHQ:APA91bGvFw7dv-qxANP6ZZANcO8X3pdyvXM0F2ICkPdiz-VB5f4tznepuk0wNn1e_17-QKNcl_odgsWOxyEBGZHEzylyjOn9nhqFB9NNnKSnXXhKBY4f2PFrl6H4f7T3qRx9CM02JDlB'
    deviceToken = token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {
        'notification': {'title': 'Evas-SOS',
                         'body': msg
                         },
        'to':
        deviceToken,
            'priority': 'high',
        'data': {
            'title': 'Evas-SOS',
        }


    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    print(response.status_code)
