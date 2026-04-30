#!/bin/bash
# 直播数据采集 PoC 测试脚本

cd /home/nicola/.openclaw/workspace/skills/live-stream-agent
python3 poc_data_collector.py --live-id TEST123 --interval 2 --duration 10
