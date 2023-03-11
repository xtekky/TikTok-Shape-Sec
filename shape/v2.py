from undetected_chromedriver import ChromeOptions
from flask                   import Flask, request as _request
from threading               import Thread
from time                    import time, sleep
from requests                import get

from seleniumwire.undetected_chromedriver.v2  import Chrome

app  = Flask(__name__)

def get_init_script():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.tiktok.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    return get('https://s20.tiktokcdn.com/tiktok/common/init.js?async', headers=headers, verify=False).text

@app.route('/shape', methods = ['POST'])
def shape():
    start   = time()
    headers = None
    loaded  = False
    
    driver.get('https://s20.tiktokcdn.com/tiktok/common/init.js?async')
    script = get_init_script()
    driver.execute_script(script)
    
    while not loaded:
        for request in driver.requests:
            if 'seed' in request.url:
                loaded = True
                break

    driver.execute_script('''
        fetch(`%s`, {
            headers     : {
                'authority': 'm.tiktok.com',
                'accept': '*/*',
                'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
                'cache-control': 'no-cache',
                'content-length': '0',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': '%s',
                'origin': 'https://www.tiktok.com',
                'pragma': 'no-cache',
                'referer': 'https://www.tiktok.com/',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            },
            referrer    : `https://www.tiktok.com/`,
            method      : `POST`,
            mode        : `cors`,
            credentials : `include`})''' % (_request.json['url'], _request.json['cookies']))

    while not headers:
        for request in driver.requests:
            if _request.json['url'].split('?')[0] in request.url:
                headers = request.headers
                break

    return {
        'tts'      : time() - start,
        'shape_sec': {k: v for k, v in headers.items() if k in [
            'htc6j8njvn-a',
            'htc6j8njvn-b',
            'htc6j8njvn-c',
            'htc6j8njvn-d',
            'htc6j8njvn-z',
            'htc6j8njvn-f',
        ]},
        'headers'  : {k: v for k, v in headers.items() if k in ['user-agent', 'cookie']},
    }

if __name__ == '__main__':
    opts = ChromeOptions()
    opts.add_argument("--disable-web-security")
    opts.add_argument("--user-data-dir=temp")
    driver = Chrome(options=opts, use_subprocess=True)

    Thread(target = app.run, args=('0.0.0.0', 1337,)).start()
    
    driver.get("https://s20.tiktokcdn.com/tiktok/common/init.js?async")

    print('ready')