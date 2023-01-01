import requests


req = requests.get("https://blynk.cloud/external/api/update?token=xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV&v1=250")
print(req.text)