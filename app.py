from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import subprocess
import threading
import time
import os
import signal
import json
from datetime import datetime
import queue
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局变量存储训练进程
training_processes = {}
training_logs = {}

class TrainingProcess:
    def __init__(self, process_id, script_content):
        self.process_id = process_id
        self.script_content = script_content
        self.process = None
        self.start_time = None
        self.end_time = None
        self.status = "pending"  # pending, running, completed, failed, stopped
        self.logs = []
        self.output_queue = queue.Queue()
        
    def start(self):
        try:
            # 直接执行Bash命令
            self.process = subprocess.Popen(
                self.script_content,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.start_time = datetime.now()
            self.status = "running"
            
            # 启动输出监控线程
            threading.Thread(target=self._monitor_output, daemon=True).start()
            
            return True
        except Exception as e:
            self.status = "failed"
            self.logs.append(f"启动失败: {str(e)}")
            return False
    
    def _monitor_output(self):
        try:
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'message': output.strip()
                    }
                    self.logs.append(log_entry)
                    # 通过WebSocket发送实时日志
                    socketio.emit('training_log', {
                        'process_id': self.process_id,
                        'log': log_entry
                    })
            
            # 进程结束
            return_code = self.process.poll()
            self.end_time = datetime.now()
            
            if return_code == 0:
                self.status = "completed"
            else:
                self.status = "failed"
                
            # 发送状态更新
            socketio.emit('training_status', {
                'process_id': self.process_id,
                'status': self.status,
                'end_time': self.end_time.isoformat() if self.end_time else None
            })
            
        except Exception as e:
            self.status = "failed"
            self.logs.append({
                'timestamp': datetime.now().isoformat(),
                'message': f"监控出错: {str(e)}"
            })
    
    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.status = "stopped"
                self.end_time = datetime.now()
                return True
            except:
                self.process.kill()
                self.status = "stopped"
                self.end_time = datetime.now()
                return True
        return False

@app.route('/api/start_training', methods=['POST'])
def start_training():
    try:
        data = request.json
        script_content = data.get('script', '')
        
        if not script_content.strip():
            return jsonify({'error': 'Bash命令不能为空'}), 400
        
        # 生成唯一的进程ID
        process_id = f"training_{int(time.time() * 1000)}"
        
        # 创建训练进程
        training_process = TrainingProcess(process_id, script_content)
        
        if training_process.start():
            training_processes[process_id] = training_process
            
            return jsonify({
                'success': True,
                'process_id': process_id,
                'message': '训练开始'
            })
        else:
            return jsonify({'error': '启动训练失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop_training', methods=['POST'])
def stop_training():
    try:
        data = request.json
        process_id = data.get('process_id')
        
        if process_id not in training_processes:
            return jsonify({'error': '训练进程不存在'}), 404
            
        training_process = training_processes[process_id]
        
        if training_process.stop():
            return jsonify({
                'success': True,
                'message': '训练已停止'
            })
        else:
            return jsonify({'error': '停止训练失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_processes', methods=['GET'])
def get_processes():
    try:
        processes_info = []
        for process_id, process in training_processes.items():
            info = {
                'process_id': process_id,
                'status': process.status,
                'start_time': process.start_time.isoformat() if process.start_time else None,
                'end_time': process.end_time.isoformat() if process.end_time else None,
                'logs_count': len(process.logs)
            }
            processes_info.append(info)
        
        return jsonify({
            'success': True,
            'processes': processes_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_logs/<process_id>', methods=['GET'])
def get_logs(process_id):
    try:
        if process_id not in training_processes:
            return jsonify({'error': '训练进程不存在'}), 404
            
        training_process = training_processes[process_id]
        
        return jsonify({
            'success': True,
            'logs': training_process.logs,
            'status': training_process.status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_process/<process_id>', methods=['DELETE'])
def delete_process(process_id):
    try:
        if process_id not in training_processes:
            return jsonify({'error': '训练进程不存在'}), 404
            
        training_process = training_processes[process_id]
        
        # 如果进程还在运行，先停止
        if training_process.status == 'running':
            training_process.stop()
        
        # 删除进程记录
        del training_processes[process_id]
        
        return jsonify({
            'success': True,
            'message': '进程已删除'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print('客户端已连接')

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5050)