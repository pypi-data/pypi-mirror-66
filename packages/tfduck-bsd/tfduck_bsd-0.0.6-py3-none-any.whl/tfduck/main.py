import sys
import getopt
import requests
import zipfile
import os
import shutil
import base64


def remove_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass

def check_project(project_path):
    config_path = os.path.join(project_path, "config.py")
    dag_path = os.path.join(project_path, "dag.py")
    if not os.path.exists(dag_path) or not os.path.exists(config_path):
        raise Exception("同步路径错误，同步路径应该在工程文件夹内")
    # 获取 uuid
    config_path = os.path.join(project_path, "config.py")
    with open(config_path, 'rb') as r:
        compile_obj = compile(r.read(), "", 'exec')
    ns = {}
    exec(compile_obj, ns, ns)
    config = ns["config"]
    project_id = config.get("pid", None)
    if not project_id:
        raise Exception("工程配置pid不存在")
    return project_id


def compress(folder_path="./"):
    """
    @des:-------------------------------------------------------
    import shutil
    shutil.make_archive(base_name, format, root_dir, base_dir)
    #
    base_name，是加上完整路径（不能缩写）的文件或文件夹名
    format一般是zip，其它tar之类也行
    root_dir是要压缩的目录或文件
    base_dir是压缩包里的文件层级。如你写a/b/c，这样所有文件都会塞到最底层的c文件夹中。
    """
    # 目录验证
    current_path = os.path.abspath(folder_path)
    # parent_path = os.path.dirname(current_path)
    project_id = check_project(current_path)
    #
    project_name = os.path.basename(current_path)
    zip_file_path = os.path.join(current_path, f"{project_name}")
    real_file_path = shutil.make_archive(
        zip_file_path, "zip", current_path, "./")
    # print(real_file_path)
    return real_file_path, project_id


def sync(username, password):
    real_file_path, project_id = compress("./")
    try:
        with open(real_file_path, "rb") as r:
            b64_content = base64.b64encode(r.read()).decode()
            # content = base64.b64decode(b64_content) # django view 通过这个解码即可得到二进制数据
    finally:
        remove_file(real_file_path)
    #
    data = {"username": username, "password": password,
            "project": b64_content, "project_id": project_id}
    res = requests.post(url="http://localhost:8000/syncreproject",
                        data=data)
    print(res.text)


def main(*args, **kwargs):
    help_doc = """
    -h 查看帮助文件
    create [project name] 创建工程
    sync 同步工程到服务器,配合-u和-p参数
    -v 查看版本
    -u 用户名
    -p 密码
    example:
    同步当前工程
    tfduck -uyx -p1 sync
    """
    # print(1111)
    # print(args)
    # print(kwargs)
    #
    opts, args = getopt.getopt(args, "hvu:p:d:", ["sync", "create=", "help"])
    print(opts, args)
    try:
        username = None
        password = None
        is_sync = False
        is_create = False
        for op, value in opts:
            if op == "-h":
                print(help_doc)
            elif op == "-v":
                import tfduck
                print(tfduck.__version__)
            elif op == "-u":
                username = value
            elif op == "-p":
                password = value
        try:
            arg = args[0]
        except:
            arg = None
        try:
            arg_value = args[1]
        except:
            arg_value = None
        if arg == "sync":
            is_sync = True
        elif arg == "create":
            is_create = True
            if not arg_value:
                raise Exception("create命令必须有一个工程名参数")
        if is_sync:
            sync(username, password)
    except Exception as e:
        print(e)
        print(help_doc)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
