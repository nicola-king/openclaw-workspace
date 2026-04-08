---
name: rust-bridge
version: 1.0.0
description: rust-bridge skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Rust Bridge Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 素问
> **状态**: ✅ 已激活 | **优先级**: P3-05

---

## 📋 功能概述

提供 Rust 代码编译和执行能力，支持高性能工具开发。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `rustc compile` | 编译 Rust | `rustc compile --file main.rs` |
| `cargo new` | 创建项目 | `cargo new myproject` |
| `cargo build` | 构建项目 | `cargo build --release` |
| `cargo run` | 运行项目 | `cargo run` |
| `cargo test` | 运行测试 | `cargo test` |
| `cargo add` | 添加依赖 | `cargo add serde --features derive` |
| `rust eval` | 执行代码片段 | `rust eval --code 'println!("Hello")'` |

---

## 📝 使用示例

### 示例 1: 编译单文件

```bash
# 太一，编译这个 Rust 文件
rustc compile --file hello.rs
./hello
```

**hello.rs**:
```rust
fn main() {
    println!("Hello, Taiyi AGI!");
}
```

### 示例 2: 创建新项目

```bash
# 太一，创建一个新的 Rust 项目
cargo new my_cli_tool
cd my_cli_tool
cargo add clap --features derive
```

### 示例 3: 执行代码片段

```bash
# 太一，快速执行这段 Rust 代码
rust eval --code '
fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let sum: i32 = nums.iter().sum();
    println!("Sum: {}", sum);
}
'
```

**输出**:
```
Sum: 15
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `rustc compile` (单文件)
- [x] `cargo build/run/test`
- [x] `rust eval` (无系统调用)

### 需要确认的操作
- [ ] `rust eval` (系统调用/文件 IO)
- [ ] `cargo run` (网络访问)
- [ ] 执行二进制文件 (非编译目录)

---

*创建时间：2026-04-03 09:31 | 素问 | 太一 AGI v5.0*
