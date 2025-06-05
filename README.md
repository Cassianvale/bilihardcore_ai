# BiliHardcore_AI

## 🚀 B站硬核会员自动答题工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

> 🤖 基于 LLM 的 B 站硬核会员智能答题助手，支持多种主流AI模型，自动化完成答题流程

基于原仓库 [bilibili-AIHardcore](https://github.com/NekoMirra/bilibili-AIHardcore) 进行优化改进

## ✨ 主要特性

- 🧠 **多模型支持**：支持 DeepSeek、Gemini、OpenAI 等多种 LLM 模型
- 🔐 **安全可靠**：仅调用官方 API，不上传个人信息
- 🎯 **智能答题**：利用 AI 技术提高答题准确率
- 💾 **配置记忆**：自动保存配置信息，无需重复输入
- 🖼️ **图形界面**：简洁友好的用户界面

## 📷 预览界面

<div align="center">
  <img src="https://github.com/Cassianvale/bilihardcore_ai/raw/main/assets/app_1.png" width="80%" alt="主页界面">
</div>
<div align="center">
  <img src="https://github.com/Cassianvale/bilihardcore_ai/raw/main/assets/app_2.png" width="80%" alt="配置界面">
</div>

## 🤖 支持的AI模型

| 模型 | 状态 | 特点 | 推荐度 |
|------|------|------|--------|
| **DeepSeek V3** | ✅ 推荐 | 速度快，准确率高 | ⭐⭐⭐⭐⭐ |
| **Gemini 2.0-flash** | ✅ 可用 | 准确率高，但有5秒间隔防风控 | ⭐⭐⭐⭐ |
| **OpenAI系列** | ✅ 支持 | 支持自定义API地址和模型 | ⭐⭐⭐⭐ |
| **其他兼容API** | ✅ 支持 | 火山引擎、硅基流动等 | ⭐⭐⭐ |

> ⚠️ **注意**：请避免使用类似 `DeepSeek R1` 的思考模型，思维链过长可能导致请求超时

## 🚀 快速开始

### 📋 环境要求

- Python 3.10+
- Windows / macOS / Linux

### 📦 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Cassianvale/bilihardcore_ai
   cd bilihardcore_ai
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
   ```

3. **启动程序**
   ```bash
   python run.py
   ```

## 📖 使用指南

### 🔧 配置流程

1. **选择AI模型** - 从支持的模型中选择一个
2. **输入API Key** - 填入对应模型的API密钥
3. **扫码登录** - 扫描二维码登录B站账号
4. **选择分类** - 输入要答题的分类
5. **验证码识别** - 查看并输入图形验证码
6. **开始答题** - 程序自动进行答题

### 💡 使用技巧

- 📚 **历史分区答题准确率更高**，建议优先选择
- 🔄 **程序支持断点续答**，异常中断后可继续之前的进度
- ⏱️ **合理控制频率**，避免触发平台限制

## ❓ 常见问题

<details>
<summary><b>🔍 二维码显示异常</b></summary>

**问题**：二维码乱码或无法显示  
**解决方案**：
- 在 Windows Terminal 中运行程序
- 或手动生成二维码进行扫码
</details>

<details>
<summary><b>📊 答题准确率不高</b></summary>

**问题**：答题经常不及格  
**解决方案**：
- 优先选择历史分区答题
- 尝试切换其他AI模型
- 检查网络连接质量
</details>

<details>
<summary><b>🤖 AI响应异常</b></summary>

**问题**：AI回复"无法确认"或"我不清楚"  
**解决方案**：
- 手动在B站APP完成卡住的题目
- **注意**：切勿点击返回按钮，会结束答题
</details>

<details>
<summary><b>🌐 Gemini模型问题</b></summary>

**问题**：429错误或程序直接退出  
**解决方案**：
- 稍等片刻后重新运行
- 切换网络节点（修改IP）
- 使用大陆及香港以外的网络节点
- 考虑换用DeepSeek等其他模型
</details>

## ⚠️ 重要提醒

- 🔑 **API密钥安全**：请妥善保管您的API Key，避免泄露
- 📁 **配置文件**：程序配置保存在 `~/用户目录/.bili-hardcore`，如遇问题可清空重试
- 🌍 **网络环境**：使用Gemini模型需确保网络环境符合其服务区域要求
- 📜 **合规使用**：请遵守B站相关规则，合理使用本工具
- 🔒 **隐私保护**：本工具仅调用B站接口和LLM API，不会收集或上传个人信息

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)




