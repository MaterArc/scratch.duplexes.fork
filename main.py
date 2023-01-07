import random
import requests
import threading
from flask import Flask

app = Flask(__name__)


views = 0


def add_view():
    global views
    views += 1

# Get proxies from  https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
request = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt")
with open("/tmp/proxy.txt", "w") as f:
    f.write(request.text)




def botter(username,id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "https://scratch.mit.edu/",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }
    with open("/tmp/proxy.txt", "r") as f:
        proxies = f.read().splitlines()
    while True:
        # Get random proxy
        for proxy in random.choices(proxies, k=1):
            try:
                r = requests.options(f"https://api.scratch.mit.edu/users/{username}/projects/{id}/views", proxies={"https": proxy, "http": proxy}, timeout=7)
                q = requests.post(f"https://api.scratch.mit.edu/users/{username}/projects/{id}/views", proxies={"https": proxy, "http": proxy}, headers=headers, timeout=7)
                if r.status_code == 200 and q.status_code == 200:
                    add_view()
                    print(f"View added! Total views: {views}")
                else:
                    print(f"Error: {r.status_code} {q.status_code}")
                    proxies.remove(proxy)
            except Exception as e:
                if 'HTTPSConnectionPool' in str(e):
                    proxies.remove(proxy)
                elif 'Connection aborted' in str(e):
                    proxies.remove(proxy)
                else:
                    print(e)
                    proxies.remove(proxy)

# Create an api route to start the function botter get the username and id from the url
@app.route("/<username>/<id>")
def start(username, id):
    # Star a bunch of threads
    for i in range(1000000):
        threading.Thread(target=botter, args=(username, id)).start()
    return "Started!"


