from undetected_chromedriver import ChromeOptions
from flask                   import Flask, request as _request
from threading               import Thread
from time                    import time, sleep
from requests                import get

from seleniumwire.undetected_chromedriver.v2  import Chrome

app  = Flask(__name__)
is_refreshing = False

@app.route('/init')
def init():
    return '''
        <head>
            <script src="https://s20.tiktokcdn.com/tiktok/common/init.js?async"></script>
        </head>
    '''

@app.route('/shape', methods = ['POST'])
def shape():
    start   = time()
    headers = None
    refresh = False
    
    driver.refresh()

    while not refresh:
        for request in driver.requests:
            if 'seed' in request.url:
                refresh = True
                break

    driver.execute_script('''
        fetch(`%s`, {
            referrer    : `https://www.tiktok.com/`,
            method      : `POST`,
            mode        : `cors`,
            credentials : `include`})''' % _request.json['url'])

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
    
def refresh_loop():
    global is_refreshing
    while True:
        sleep(10)
        
        is_refreshing = True
        refresh = False
        driver.refresh()
    
        while not refresh:
            for request in driver.requests:
                if 'seed' in request.url:
                    refresh = True
                    break
                
        is_refreshing = False

if __name__ == '__main__':
    opts = ChromeOptions()
    opts.add_argument("--disable-web-security")
    opts.add_argument("--user-data-dir=temp")
    driver = Chrome(options=opts, use_subprocess=True)

    Thread(target = app.run, args=('0.0.0.0', 1337,)).start()
    
    driver.get('http://localhost:1337/init')
    
    # Thread(target = refresh_loop).start()
    print('ready')