#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/feishu-integration')
from bitable_importer import FeishuBitableImporter

importer = FeishuBitableImporter()
result = importer.import_file('/home/nicola/.openclaw/workspace/test_import.xlsx')
print(f'导入结果：{result}')
