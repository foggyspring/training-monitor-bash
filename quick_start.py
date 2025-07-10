#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
训练监视器一键启动脚本
同时启动前端和后端服务
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
import signal

class TrainingMonitorLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def start_backend(self):
        """启动Flask后端服务"""
        print("🚀 启动后端服务器...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # 监控后端输出
            for line in iter(self.backend_process.stdout.readline, ''):
                if not self.running:
                    break
                print(f"[后端] {line.strip()}")
                
        except Exception as e:
            print(f"❌ 后端启动失败: {e}")

    def start_frontend(self):
        """启动前端HTTP服务器"""
        print("🌐 启动前端服务器...")
        try:
            # 启动HTTP服务器
            self.frontend_process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', '8080'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # 等待服务器启动
            time.sleep(2)
            
            # 自动打开浏览器
            frontend_url = "http://localhost:8080/vue_frontend.html"
            print(f"🌐 前端地址: {frontend_url}")
            
            try:
                webbrowser.open(frontend_url)
                print("✅ 已自动打开浏览器")
            except:
                print("⚠️  请手动打开浏览器访问上述地址")
                
        except Exception as e:
            print(f"❌ 前端启动失败: {e}")

    def check_files(self):
        """检查必要文件是否存在"""
        required_files = ['app.py', 'vue_frontend.html']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            print("请确保在包含app.py和vue_frontend.html的目录中运行此脚本")
            return False
        
        return True

    def cleanup(self):
        """清理进程"""
        print("\n🧹 正在清理...")
        self.running = False
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
            except:
                self.backend_process.kill()
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
            except:
                self.frontend_process.kill()
        
        print("✅ 清理完成")

    def start(self):
        """启动所有服务"""
        print("🚀 训练监视器启动器")
        print("=" * 50)
        
        # 检查文件
        if not self.check_files():
            return
        
        try:
            # 在后台线程启动后端
            backend_thread = threading.Thread(target=self.start_backend, daemon=True)
            backend_thread.start()
            
            # 等待后端启动
            time.sleep(3)
            
            # 启动前端
            self.start_frontend()
            
            print("\n" + "=" * 50)
            print("🎉 启动完成！")
            print("\n📋 服务信息:")
            print("🔗 后端API: http://localhost:5050")
            print("🌐 前端页面: http://localhost:8080/vue_frontend.html")
            print("\n💡 使用说明:")
            print("1. 在网页中输入Bash训练命令")
            print("2. 点击'开始训练'按钮")
            print("3. 实时查看训练日志")
            print("4. 可随时停止或删除进程")
            print("\n⚠️  按Ctrl+C停止所有服务")
            print("=" * 50)
            
            # 保持运行
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 收到停止信号...")
        
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """信号处理器"""
    print("\n👋 收到停止信号，正在关闭...")
    sys.exit(0)

def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动服务
    launcher = TrainingMonitorLauncher()
    launcher.start()

if __name__ == "__main__":
    main()