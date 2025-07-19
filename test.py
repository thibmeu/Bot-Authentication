import requests

res = requests.get("https://medium.com/@ebimsv/building-python-packages-07fbfbb959a9")
print(res.headers)