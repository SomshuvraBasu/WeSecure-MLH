import requests

def sendImg(image, id):

    apiToken = 'API_TOKEN'
    chatID = id
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto'
    params = {'chat_id': chatID}
    files = {'photo': image}

    try:
        response = requests.post(apiURL, params, files=files)
        print(response.text)
    except Exception as e:
        print(e)

def main(id):
    #open image file
    image = open('Attendance.png','rb')
    sendImg(image,id)