import subprocess
import sys
import os

def main():
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 安装依赖
    print("正在安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 启动Flask应用
    print("正在启动Flask应用...")
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    main()