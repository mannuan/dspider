import requests
while(True):
    try:
        response = requests.get(url='http://fund.eastmoney.com/', timeout=10)
        page = response.content.decode('utf-8')
        print(page)
        break
    except Exception:
        pass