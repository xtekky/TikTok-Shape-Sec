from time            import time, sleep
from tls_client      import Session
from requests        import get, post
from urllib.parse    import urlencode
from re              import findall
# from utils.info      import mssdk_info
from utils.report    import report_enc
from utils.body      import get_body
from utils.ressource import enc_eq
from utils.bogus     import Signer
from json            import loads, dumps

while True:

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    client     = Session(client_identifier='chrome_111')
    # client.proxies = {
    #     'http'  : 'http://',
    #     'https' : 'http://'
    # }

    sessionid  = ''

    client.headers = {
        "host"              : "mssdk-va.tiktok.com",
        "connection"        : "keep-alive",
        "sec-ch-ua"         : "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
        "sec-ch-ua-mobile"  : "?0",
        "user-agent"        : user_agent,
        "sec-ch-ua-platform": "\"macOS\"",
        "accept"            : "*/*",
        "origin"            : "https://www.tiktok.com",
        "sec-fetch-site"    : "same-site",
        "sec-fetch-mode"    : "cors",
        "sec-fetch-dest"    : "empty",
        "referer"           : "https://www.tiktok.com/",
        "accept-encoding"   : "application/json",
        "accept-language"   : "en-GB,en-US;q=0.9,en;q=0.8",
    }
    client.cookies['sessionid'] = sessionid

    init      = client.get('https://www.tiktok.com')
    device_id = findall(r'wid":"([0-9]+)"', init.text)[0]

    if not client.cookies.get_dict().get('msToken'): client.get(f'https://mssdk-va.tiktok.com/web/resource', params = {
            'eq': enc_eq(urlencode({
                'aid'       : 1988,
                'region'    : 'va-tiktok',
                'location'  : 'www.tiktok.com'
            }))
        })

    params = Signer.sign(f'msToken={client.cookies.get_dict()["msToken"]}', client.headers['user-agent'])
    resp   = client.post(f"https://mssdk-va.tiktok.com/web/report?{params}", json = {
        "magic"         : 538969122,
        "version"       : 1,
        "dataType"      : 8,
        "strData"       : report_enc(get_body()),
        "tspFromClient" : int(time() * 1000)
    })

    print(resp.text.encode())

    print(client.cookies.get_dict()["msToken"])

    def get_shape(url):
        resp = post('http://localhost:1337/shape', json = {
            'url': url
        })

        return resp.json()['shape_sec']

    sleep(2)



    params = Signer.sign(urlencode({
        "aid": "1988",
        "app_language": "en",
        "app_name": "tiktok_web",
        "aweme_id": 7205987592741932294,
        "battery_info": "0.73",
        "browser_language": "en",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "MacIntel",
        "browser_version": "5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F111.0.0.0%20Safari%2F537.36",
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        "device_id": device_id,
        "device_platform": "web_pc",
        "focus_state": "true",
        "from_page": "video",
        "history_len": "4",
        "is_fullscreen": "true",
        "is_page_visible": "true",
        "os": "mac",
        "priority_region": "FR",
        "referer": "",
        "region": "IE",
        "screen_height": "956",
        "screen_width": "1470",
        "type": "1",
        "tz_name": "Europe%2FDublin",
        "webcast_language": "en", 
        "msToken": client.cookies.get_dict()['msToken']}), user_agent)

    url = f'https://m.tiktok.com/api/commit/item/digg/?{params}'
    
    # 'htc6j8njvn-a',
    # 'htc6j8njvn-b',
    # 'htc6j8njvn-c',
    # 'htc6j8njvn-d',
    # 'htc6j8njvn-z',
    # 'htc6j8njvn-f',

    headers = get_shape(url) | {
        'authority': 'm.tiktok.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'content-length': '0',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://www.tiktok.com',
        'referer': 'https://www.tiktok.com/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent
    }

    response = client.post(url, headers=headers, data='')
    print(response.text)
    
    if response.json()['is_digg'] == 0:
        print('liked')
        break
