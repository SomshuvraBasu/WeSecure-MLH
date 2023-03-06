import requests
import random

apiToken = 'API_TOKEN'
url = f"https://api.telegram.org/bot{apiToken}/getUpdates"
response = requests.get(url)
data=response.json()
id_no = []
text = []

def readText() :
    
    # user_dict={}
    # LEA_dict={}
    
    for i in data['result']:
        # if i['message']['text'] not in user_dict.values():
        #     k=10*random.randint(1,100000)
        #     if i['message']['text']=="/start":
        #         k+=6
        #     elif i['message']['text']=="/lea":
        #         k+=1
        #     user_dict[k]=[i['message']['from']['first_name'],i['message']['text']]
        # user_dict[random.randint(1,1000000)]=[i['message']['from']['first_name'],i['message']['chat']['id']]

        id_no.append(i['message']['chat']['id'])
        text.append(i['message']['text'])

def getText(sid):
    readText()
    for i in range(len(id_no)-1,-1,-1):
        if id_no[i]==sid:
            return text[i]

# get_IdNo_and_Text(url, id_no, text)

# length = len(id_no)
# for i in range(length) :
#     print(str(id_no[i]) + " " + str(text[i]))