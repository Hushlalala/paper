import requests
def send_pushplus_message(token, title, content):
    url = 'http://www.pushplus.plus/send'
    data = {
       "token": token,
       "title": title,
       "content": content
   }
    response = requests.post(url, json=data)
    return response.json()

token = 'e8979a20686f4175b2e2cc509d732a48'
title = 'Test Message'
content = 'This is a test message from  pushplus.'
result = send_pushplus_message(token, title, content)
print(result)
