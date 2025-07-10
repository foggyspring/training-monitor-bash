# 训练进程监视器（Bash命令版）

本项目是一个支持通过网页输入Bash命令来启动和监控训练进程的可视化工具。前端基于Vue，后端基于Flask + Flask-SocketIO，支持实时日志推送。

## 功能简介
- 网页输入任意Bash训练命令（如 `python train.py --epochs 5`）
- 实时查看训练日志和进度
- 支持停止、删除训练进程
- 多进程管理

## 目录结构
```
├── app.py                # 后端 Flask + SocketIO 服务
├── quick_start.py        # 一键启动前后端脚本
├── vue_frontend.html     # 前端页面（直接用http.server静态服务）
├── train.py              # 测试用训练脚本（可自定义Bash命令调用）
```

## 安装依赖
建议使用 Python 3.7+，并提前安装以下依赖：

```bash
pip install flask flask_cors flask_socketio
```

## 启动方法
1. **一键启动（推荐）**
   ```bash
   python quick_start.py
   ```
   启动后会自动打开前端页面。

2. **手动启动**
   - 启动后端：
     ```bash
     python app.py
     ```
   - 启动前端静态服务：
     ```bash
     python -m http.server 8080
     ```
   - 浏览器访问：
     [http://localhost:8080/vue_frontend.html](http://localhost:8080/vue_frontend.html)

## 使用说明
- 在网页输入框输入Bash训练命令（如 `python train.py --epochs 5`）
- 点击“开始训练”即可实时监控日志
- 可随时停止或删除进程

## 测试脚本
- `train.py` 为模拟训练脚本，支持常见参数，可用于测试

---
如遇端口占用或依赖缺失，请根据终端提示处理。 