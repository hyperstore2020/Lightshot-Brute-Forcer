from colors import green, red, reset
import threading, requests, random, string, sys, os; from time import sleep

os.system('title [Lightshot Brute Forcer] - Scrape Screenshots ^| Loading...')
if not os.path.exists('Images'): os.makedirs('Images')

valid = 0
invalid = 0
retries = 0
proxies = []
proxy_num = 0
lock = threading.Lock()

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def grab_proxies():
    while True:
        all_proxies = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&ssl=all&anonymity=all').text
        for proxy in all_proxies.splitlines():
            proxies.append(proxy)

        sleep(600)
        proxies.clear()

def cpm():
    old = valid + invalid
    sleep(1)
    new = valid + invalid
    return ((new - old) * 60)


def save(arg):
    content = requests.get(arg).content
    if 'image.prntscr' in arg: half_url = 'https://image.prntscr.com/image/'
    elif 'i.imgur' in arg: half_url = 'https://i.imgur.com/'
    with open('Images/' + arg.replace(half_url, '')[:6] + '.png', 'wb') as f: f.write(content)

def main(proxy):
    global valid
    global invalid
    global retries

    code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    try:
        check = requests.get('https://prnt.sc/%s' % (code), headers = headers, proxies = {'https': 'http://%s' % (proxy)}).text
    except:
        retries += 1
        os.system('title [Lightshot Brute Forcer] - Scrape Screenshots ^| Checked: %s ^| Valid: %s ^| Invalid: %s ^| Retries: %s ^| CPM: %s' % (valid + invalid, valid, invalid, retries, cpm()))
    else:
        if 'name="twitter:image:src" content="' in check and not '0_173a7b_211be8ff' in check and not 'ml3U3Pt' in check:
            lock.acquire(); sys.stdout.write('[%sVALID%s] https://prnt.sc/%s\n' % (green(), reset(), code)); lock.release()
            valid += 1
            os.system('title [Lightshot Brute Forcer] - Scrape Screenshots ^| Checked: %s ^| Valid: %s ^| Invalid: %s ^| Retries: %s ^| CPM: %s' % (valid + invalid, valid, invalid, retries, cpm()))
            url = check.split('name="twitter:image:src" content="')[1].split('"/> <meta')[0]
            save(url)
            with open('Image Links.txt', 'a', encoding = 'UTF-8') as f: f.write('https://prnt.sc/%s\n' % (code))
        else:
            lock.acquire(); sys.stdout.write('[%sINVALID%s] https://prnt.sc/%s\n' % (red(), reset(), code)); lock.release()
            invalid += 1
            os.system('title [Lightshot Brute Forcer] - Scrape Screenshots ^| Checked: %s ^| Valid: %s ^| Invalid: %s ^| Retries: %s ^| CPM: %s' % (valid + invalid, valid, invalid, retries, cpm()))

threading.Thread(target = grab_proxies).start()
threading.Thread(target = cpm).start()
sleep(3)

while True:
    if threading.active_count() <= 200:
        try:
            threading.Thread(target = main, args = (proxies[proxy_num],)).start()
            proxy_num += 1
            if proxy_num >= len(proxies):
                proxy_num = 0
        except:
            pass
