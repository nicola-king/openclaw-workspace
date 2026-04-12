#!/usr/bin/env python3
"""
百度网盘管理 API - 太一集成

作者：太一 AGI
创建：2026-04-10
"""

from flask import Flask, jsonify, request
from baidu_client import client

APP = Flask(__name__)

@APP.route('/api/baidu/status')
def api_status():
    """获取百度网盘状态"""
    return jsonify(client.get_status())

@APP.route('/api/baidu/quota')
def api_quota():
    """获取配额"""
    return jsonify(client.get_quota())

@APP.route('/api/baidu/list', methods=['GET'])
def api_list():
    """列出文件"""
    path = request.args.get('path', '/apps/taiyi')
    return jsonify(client.list_dir(path))

@APP.route('/api/baidu/upload', methods=['POST'])
def api_upload():
    """上传文件"""
    data = request.json
    local_path = data.get('local_path')
    remote_path = data.get('remote_path', '/apps/taiyi')
    
    if not local_path:
        return jsonify({"error": "需要 local_path 参数"}), 400
    
    return jsonify(client.upload(local_path, remote_path))

@APP.route('/api/baidu/download', methods=['POST'])
def api_download():
    """下载文件"""
    data = request.json
    remote_path = data.get('remote_path')
    local_path = data.get('local_path')
    
    if not remote_path:
        return jsonify({"error": "需要 remote_path 参数"}), 400
    
    return jsonify(client.download(remote_path, local_path))

@APP.route('/api/baidu/backup', methods=['POST'])
def api_backup():
    """备份工作区"""
    data = request.json or {}
    exclude_dirs = data.get('exclude_dirs')
    return jsonify(client.backup_workspace(exclude_dirs))

@APP.route('/api/baidu/sync', methods=['POST'])
def api_sync():
    """从网盘同步"""
    data = request.json or {}
    remote_dir = data.get('remote_dir', '/apps/taiyi/workspace')
    return jsonify(client.sync_from_netdisk(remote_dir))

@APP.route('/api/baidu/search', methods=['GET'])
def api_search():
    """搜索文件"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({"error": "需要 keyword 参数"}), 400
    return jsonify(client.search(keyword))

@APP.route('/api/baidu/mkdir', methods=['POST'])
def api_mkdir():
    """创建目录"""
    data = request.json
    remote_path = data.get('path')
    
    if not remote_path:
        return jsonify({"error": "需要 path 参数"}), 400
    
    return jsonify(client.create_dir(remote_path))

@APP.route('/api/baidu/remove', methods=['POST'])
def api_remove():
    """删除文件"""
    data = request.json
    remote_path = data.get('path')
    
    if not remote_path:
        return jsonify({"error": "需要 path 参数"}), 400
    
    return jsonify(client.remove(remote_path))

if __name__ == '__main__':
    print("📦 百度网盘管理 API 启动中...")
    print("=" * 50)
    print(f"🌐 访问地址：http://localhost:5003")
    print()
    APP.run(host='0.0.0.0', port=5003, debug=False)
