import requests
def tokenline(message):
    global token
    token = message
def line(message):
    line_notify_token = token
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + token} 
    requests.post(line_notify_api, data=payload, headers=headers)
