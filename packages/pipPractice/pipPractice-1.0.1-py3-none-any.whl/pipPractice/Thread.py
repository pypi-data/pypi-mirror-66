# import threading
#
#
# def sum(low, high):
#     total = 0
#     for i in range(low, high + 1):
#         total += i
#     print("Subthread : ", total)
#
#
# t = threading.Thread(target=sum, args=(1, 100000))
# t.start()
#
# print("Main Thread")

import requests
import threading
import time


class HtmlGetter(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        resp = requests.get(self.url)
        time.sleep(1)
        print(self.url, len(resp.text), ' chars')


t = HtmlGetter('http://google.com')
t.start()

print("### end ###")