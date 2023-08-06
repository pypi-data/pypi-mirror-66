import sys
import getopt
import requests
import zipfile
import os
import shutil
import base64
import uuid


def remove_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass


def check_project(project_path):
    package_name = os.path.basename(project_path)
    config_path = os.path.join(project_path, f"{package_name}/config.py")
    dag_path = os.path.join(project_path, f"{package_name}/dag.py")
    if not os.path.exists(dag_path) or not os.path.exists(config_path):
        raise Exception("同步路径错误，同步路径应该在工程文件夹内")
    # 获取 uuid
    config_path = os.path.join(project_path, f"{package_name}/config.py")
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
    base_name : 创建的目标文件名，包括路径，减去任何特定格式的扩展。
    format : 压缩包格式。”zip”, “tar”, “bztar”或”gztar”中的一个。
    root_dir : 打包时切换到的根路径。也就是说，开始打包前，会先执行路径切换，切换到root_dir所指定的路径。默认值为当前路径
    base_dir : 开始打包的路径。也就是说，该命令会对base_dir所指定的路径进行打包，默认值为 root_dir ，即打包切换后的当前目录。亦可指定某一特定子目录，从而实现打包的文件包含此统一的前缀路径
    owner 和 group 为创建tar包时使用，默认为用户当前的 owner & group
    @des:----------------------------------
    unpack_archive(filename, extract_dir=None, format=None)： 解压操作。Python3新增方法
    filename：文件路径
    extract_dir：解压至的文件夹路径。文件夹可以不存在，会自动生成
    format：解压格式，默认为None，会根据扩展名自动选择解压格式
    """
    # 目录验证
    current_path = os.path.abspath(folder_path)
    parent_path = os.path.dirname(current_path)
    project_id = check_project(current_path)
    #
    project_name = os.path.basename(current_path)
    zip_file_path = os.path.join(parent_path, f"{project_name}")
    if 0:
        # 这样即可实现目录下所有文件，但不打包目录，
        # 一般配合shutil.unpack_archive(filename, "/你指定的解压目录", "zip") 来使用
        real_file_path = shutil.make_archive(
            zip_file_path, "zip", current_path, f"./")
    else:
        # 这样即可实现打包目录，解压后会生成目录
        # 一般配合shutil.unpack_archive(filename, "/你指定的解压目录的父目录", "zip") 来使用
        real_file_path = shutil.make_archive(
            zip_file_path, "zip", parent_path, f"./{project_name}")
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
    data = {"username": username, "password": password, "is_clean": False,
            "project": b64_content, "project_id": project_id}
    res = requests.post(url="http://localhost:8000/syncreproject",
                        data=data, timeout=(60, 300))
    print(res.text)


def init(username, password):
    real_file_path, project_id = compress("./")
    try:
        with open(real_file_path, "rb") as r:
            b64_content = base64.b64encode(r.read()).decode()
            # content = base64.b64decode(b64_content) # django view 通过这个解码即可得到二进制数据
    finally:
        remove_file(real_file_path)
    #
    data = {"username": username, "password": password, "is_init": True,
            "project": b64_content, "project_id": project_id}
    res = requests.post(url="http://localhost:8000/syncreproject",
                        data=data, timeout=(60, 300))
    print(res.text)


def create_project(username, password, package_name):
    """
    @des: 创建工程模板
    """
    # 判断工程是否存在
    if os.path.exists(f"./{package_name}"):
        print(f"工程名: {package_name} 已经存在, 请确认删除后再创建！")
        return
    #
    data = {"username": username, "password": password,
            "package_name": package_name}
    res = requests.post(url="http://localhost:8000/createproject",
                        data=data, timeout=(60, 60))
    res_data = res.json()
    if res_data.get("s", 2)==1:
        file_data = res_data["file_data"]
        file_content = base64.b64decode(file_data)
        #
        try:
            tmp_file_path = f"./{uuid.uuid1().hex}.zip"
            with open(tmp_file_path, "wb") as f:
                f.write(file_content)
            real_project_path = f"./{package_name}"
            shutil.unpack_archive(
                tmp_file_path, extract_dir=real_project_path, format='zip')
        finally:
            remove_file(tmp_file_path)
        print("create project success")
    else:
        print(res_data.get('msg', "未知错误"))


def main(*args, **kwargs):
    help_doc = """
    -h 查看帮助文件
    create [project name] 创建工程
    sync 同步工程到服务器, 修改定时任务时间, 配合-u和-p参数
    init 同步工程到服务器, 并删除原来的dags和执行记录，修改定时任务时间, 配合-u和-p参数
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
        is_init = False
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
        if arg == "init":
            is_init = True
        elif arg == "create":
            is_create = True
            if not arg_value:
                raise Exception("create命令必须有一个工程名参数")
        if is_create:
            create_project(username, password, arg_value)
        if is_sync:
            sync(username, password)
        elif is_init:
            init(username, password)
    except Exception as e:
        print(e)
        print(help_doc)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
