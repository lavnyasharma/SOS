import vonage





def sms_(frm='concric',message=' ',to=' '):
    """
    from , message , to
    """
    client = vonage.Client(key="1efc8bdf", secret="aFwr60pY3olC5cEO")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": frm,
            "to": to,
            "text": message,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        return True
    print(responseData['messages'][0]['error-text'])
    raise Exception('invalid phone')