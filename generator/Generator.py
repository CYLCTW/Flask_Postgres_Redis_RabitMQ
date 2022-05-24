import requests
url = 'http://localhost:5000/sendMessage'
payload = {'user': 'Al-turar', 'message': 'hello'}

for i in range(10):
    print("Message send")
    r = requests.post(url, data=payload)
