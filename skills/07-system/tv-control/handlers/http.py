#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP API 服务器
"""

import logging
from flask import Flask, request, jsonify
from threading import Thread

logger = logging.getLogger('TVControl.HTTP')

class HTTPServer:
    """HTTP API 服务器"""
    
    def __init__(self, host, port, token, skill):
        self.host = host
        self.port = port
        self.token = token
        self.skill = skill
        self.app = Flask(__name__)
        self.thread = None
        self.running = False
        
        self._setup_routes()
        logger.info(f"🌐 HTTP API 初始化完成 (端口 {port})")
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/tv/control', methods=['POST'])
        def control():
            """电视控制 API"""
            data = request.json
            token = data.get('token', '')
            
            # 验证 token
            if token != self.token:
                return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
            
            command = data.get('command', '')
            result = self.skill.handle_command(command)
            return jsonify(result)
        
        @self.app.route('/tv/status', methods=['GET'])
        def status():
            """电视状态 API"""
            result = self.skill.get_status()
            return jsonify(result)
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """健康检查"""
            return jsonify({'status': 'ok', 'service': 'taiyi-tv-control'})
    
    def _run(self):
        """运行服务器"""
        logger.info(f"🚀 HTTP API 启动在 {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
    
    def start(self):
        """启动服务器"""
        self.running = True
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("✅ HTTP API 已启动")
    
    def stop(self):
        """停止服务器"""
        self.running = False
        logger.info("⏹️ HTTP API 已停止")
