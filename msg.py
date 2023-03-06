import requests
import creds

apiURL = f'https://api.telegram.org/bot{creds.apiToken}/sendMessage'
StreamLink = f"Video Stream Link:{creds.StreamLink}"
DeviceLocation = f"Device Location:{creds.device_location}"

def send_Img(image, apiURL, chatID):
    params = {'chat_id': chatID}
    files = {'photo': image}

    try:
        response = requests.post(apiURL, params=params, files=files)
        print(response.text)
    except Exception as e:
        print(e)


def send_Text(msg, apiURL, chatID):
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': msg})
        print(response.text)
    except Exception as e:
        print(e)


def fam_Msg(state, name=None, img=None):
    chatID = creds.family_chatID
    if state == 1:
        msg = f"Familiar face detected--{name}--logged ✅✅ "
        send_Text(msg, apiURL, chatID)
    elif state == 2:
        msg = f"Suspicious face detected--{name}--lea notified ❌🚨"
        send_Text(msg, apiURL, chatID)
        msg = f"{StreamLink}"
        send_Text(msg, apiURL, chatID)
    elif state == 3:
        msg = "Unknown face detected--awaiting response 🔍☎️"
        send_Text(msg, apiURL, chatID)
        # msg = "Choose Response"
        # send_Text(msg, apiURL, chatID)

        msg = f"{StreamLink}"
        send_Text(msg, apiURL, chatID)

        # receive input from family
        # if input == 1:
        #   treat as suspected
        # else:
        #   continue

    elif state==4:
        # this segement is still under developement
        # as a future enhancement we would like to implement features like
        # mask detection etc
        msg = "Face not detectable"
        send_Text(msg, apiURL, chatID)
        msg = "Volunteer Informed"
        send_Text(msg, apiURL, chatID)
        # imgOpen=open(img,'rb')
        # send_Img(imgOpen, apiURL, chatID)
        msg = f"{StreamLink}"
        send_Text(msg, apiURL, chatID)
        # receive input from family
        # if input == 1:
        #   treat as suspected
        # else:
        #   continue


def lea_Msg(state, name, img):
    chatID = creds.lea_chatID
    if state == 1:
        pass
    elif state == 2:
        msg = f"Suspicious face detected--{name}--lea notified ❌🚨"
        send_Text(msg, apiURL, chatID)
        # imgOpen=open(img,'rb')
        # send_Img(imgOpen, apiURL, chatID)
        msg = f"{DeviceLocation}"
        send_Text(msg, apiURL, chatID)
        msg = f"{StreamLink}"
        send_Text(msg, apiURL, chatID)
    elif state == 3:
        pass
    elif state==4:
        pass

def volunteer_Msg(state, name, img):
    chatID = creds.volunteer_chatID
    if state == 1:
        pass
    elif state == 2:
        msg = f"Suspicious face detected--{name}--lea notified ❌🚨"
        send_Text(msg, apiURL, chatID)
        msg = f"{DeviceLocation}"
        send_Text(msg, apiURL, chatID)
    elif state == 3:
        msg = "Unknown face--awaiting action--Please Assist 🔍☎️"
        send_Text(msg, apiURL, chatID)
        msg = f"{StreamLink}"
        send_Text(msg, apiURL, chatID)
        # If input from family is 1
        # treat as suspected
        # else do nothing
        pass
    elif state==4:
        msg = "Face can't be detected--assistance needed"
        send_Text(msg, apiURL, chatID)
        msg = f"{DeviceLocation}"
        send_Text(msg, apiURL, chatID)

def send(state, name=None, img=None):
    fam_Msg(state, name, img)
    lea_Msg(state, name, img)
    volunteer_Msg(state, name, img)
