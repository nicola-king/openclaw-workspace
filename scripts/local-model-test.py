#!/usr/bin/env python3
"""
太一本地模型性能测试脚本
测试 Ollama、llama.cpp、TurboQuant 的性能基准
"""

import subprocess
import time
import json
import sys

def test_ollama(model="gemma2:9b-instruct-q4_K_M", prompt="你好"):
    """测试 Ollama 推理性能"""
    print(f"\n🧪 测试 Ollama: {model}")
    print("=" * 50)
    
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        elapsed = time.time() - start
        output = result.stdout.strip()
        tokens = len(output.split())
        
        print(f"✅ 响应时间：{elapsed:.2f}s")
        print(f"✅ 输出长度：{len(output)} 字符 / {tokens} tokens")
        print(f"✅ 推理速度：{tokens/elapsed:.2f} tokens/s")
        print(f"\n📝 输出预览:\n{output[:200]}...")
        
        return {
            "status": "success",
            "elapsed": elapsed,
            "tokens": tokens,
            "speed": tokens/elapsed,
            "output": output
        }
    except subprocess.TimeoutExpired:
        print("❌ 超时 (120s)")
        return {"status": "timeout"}
    except Exception as e:
        print(f"❌ 错误：{e}")
        return {"status": "error", "error": str(e)}

def test_llama_cpp(model_path, prompt="你好"):
    """测试 llama.cpp 推理性能"""
    print(f"\n🧪 测试 llama.cpp: {model_path}")
    print("=" * 50)
    
    llama_cli = "/home/nicola/.openclaw/workspace/llama.cpp/build/bin/llama-cli"
    
    start = time.time()
    try:
        result = subprocess.run(
            [
                llama_cli,
                "-m", model_path,
                "-n", "256",
                "--n_threads", "4",
                "-p", prompt
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        elapsed = time.time() - start
        output = result.stdout.strip()
        tokens = len(output.split())
        
        print(f"✅ 响应时间：{elapsed:.2f}s")
        print(f"✅ 输出长度：{len(output)} 字符 / {tokens} tokens")
        print(f"✅ 推理速度：{tokens/elapsed:.2f} tokens/s")
        
        return {
            "status": "success",
            "elapsed": elapsed,
            "tokens": tokens,
            "speed": tokens/elapsed
        }
    except FileNotFoundError:
        print(f"❌ llama-cli 未找到：{llama_cli}")
        return {"status": "not_found"}
    except subprocess.TimeoutExpired:
        print("❌ 超时 (120s)")
        return {"status": "timeout"}
    except Exception as e:
        print(f"❌ 错误：{e}")
        return {"status": "error", "error": str(e)}

def test_turboquant():
    """测试 TurboQuant 功能"""
    print(f"\n🧪 测试 TurboQuant")
    print("=" * 50)
    
    try:
        # 激活虚拟环境并测试
        cmd = """
source /home/nicola/.openclaw/workspace/turboquant-env/bin/activate
python3 -c "
import turboquant
import torch

print(f'TurboQuant 版本：{turboquant.__version__}')

# 测试 KV Cache 压缩
kv_cache = torch.randn(100, 512, dtype=torch.float16)
print(f'原始大小：{kv_cache.numel() * 2 / 1024:.2f} KB')

compressed = turboquant.compress_kv_cache(kv_cache, bits=4)
print(f'压缩后大小：{compressed.numel() * 0.5 / 1024:.2f} KB (4-bit)')

decompressed = turboquant.decompress_kv_cache(compressed, original_shape=kv_cache.shape)
print(f'解压后大小：{decompressed.numel() * 2 / 1024:.2f} KB')

# 计算误差
error = torch.mean(torch.abs(kv_cache - decompressed)).item()
print(f'平均误差：{error:.6f}')
print('✅ TurboQuant 测试通过')
"
"""
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            timeout=60
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ stderr: {result.stderr}")
        
        return {"status": "success" if result.returncode == 0 else "error"}
    except Exception as e:
        print(f"❌ 错误：{e}")
        return {"status": "error", "error": str(e)}

def check_model_status():
    """检查模型下载状态"""
    print(f"\n📊 检查模型状态")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        if "gemma2" in result.stdout.lower():
            print("✅ Gemma 2 9B 已安装")
            return True
        else:
            print("⏳ Gemma 2 9B 下载中...")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def main():
    print("🚀 太一本地模型性能测试")
    print("=" * 60)
    print(f"时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"硬件：Intel N150 (4 核), 32GB RAM")
    print("=" * 60)
    
    results = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "hardware": "Intel N150 (4 核), 32GB RAM",
        "tests": {}
    }
    
    # 1. 检查模型状态
    model_ready = check_model_status()
    results["model_ready"] = model_ready
    
    # 2. 测试 Ollama (如果模型已安装)
    if model_ready:
        results["tests"]["ollama"] = test_ollama()
    else:
        print("\n⏭️  跳过 Ollama 测试 (模型未安装)")
        results["tests"]["ollama"] = {"status": "skipped", "reason": "model_not_installed"}
    
    # 3. 测试 TurboQuant
    results["tests"]["turboquant"] = test_turboquant()
    
    # 4. llama.cpp 测试 (需要模型文件)
    print("\n⏭️  跳过 llama.cpp 测试 (需要 GGUF 模型文件)")
    results["tests"]["llama_cpp"] = {"status": "skipped", "reason": "model_file_required"}
    
    # 保存结果
    output_file = "/home/nicola/.openclaw/workspace/reports/local-model-benchmark.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📄 结果已保存：{output_file}")
    
    # 生成摘要
    print("\n" + "=" * 60)
    print("📊 测试摘要")
    print("=" * 60)
    for test_name, result in results["tests"].items():
        status = result.get("status", "unknown")
        if status == "success":
            speed = result.get("speed", "N/A")
            print(f"✅ {test_name}: {speed} tokens/s" if isinstance(speed, (int, float)) else f"✅ {test_name}: 通过")
        elif status == "skipped":
            print(f"⏭️  {test_name}: 跳过 ({result.get('reason', '')})")
        else:
            print(f"❌ {test_name}: {status}")
    
    return results

if __name__ == "__main__":
    main()
