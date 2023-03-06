import requests
import creds

def sendImg(image, id):

    chatID = id
    apiURL = f'https://api.telegram.org/bot{creds.apiToken}/sendPhoto'
    params = {'chat_id': chatID}
    files = {'photo': image}

    try:
        response = requests.post(apiURL, params, files=files)
        print(response.text)
    except Exception as e:
        print(e)

def main(id):
    #open image file
    image = open('Visitor.png','rb')
    sendImg(image,id)