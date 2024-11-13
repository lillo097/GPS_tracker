import requests

def runBypass(url):
    #url = 'https://halloooooohdhhddh.loca.lt/'
    headers = {
        "bypass-tunnel-reminder": "true"
    }
    requests.get(url, headers=headers)

