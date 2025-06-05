#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from loguru import logger

# 模型配置 - 基础URL和默认模型
MODEL_CONFIGS = {
    'deepseek': {
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat',
        'api_key': ''
    },
    'gemini': {
        'base_url': 'https://generativelanguage.googleapis.com/v1beta',
        'model': 'gemini-2.0-flash',
        'api_key': ''
    },
    'custom': {
        'base_url': '',
        'model': '',
        'api_key': ''
    }
}

# 模型显示信息
MODEL_DISPLAY_INFO = {
    'deepseek': {
        'name': 'DeepSeek',
        'icon': '🧠',
        'choice_value': '1'
    },
    'gemini': {
        'name': 'Gemini',
        'icon': '✨',
        'choice_value': '2'
    },
    'custom': {
        'name': '自定义模型',
        'icon': '⚙️',
        'choice_value': '3'
    }
}

# 配置目录
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.bili-hardcore')

def ensure_config_dir():
    """确保配置目录存在"""
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_model_config(model_type):
    """加载模型完整配置（包括API密钥）"""
    ensure_config_dir()
    config_file = os.path.join(CONFIG_DIR, f'{model_type}_config.json')
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保返回完整的配置结构
                default_config = MODEL_CONFIGS.get(model_type, {})
                return {
                    'base_url': data.get('base_url', default_config.get('base_url', '')),
                    'model': data.get('model', default_config.get('model', '')),
                    'api_key': data.get('api_key', default_config.get('api_key', ''))
                }
        except Exception as e:
            logger.error(f'读取{model_type}配置失败: {e}')
    
    return MODEL_CONFIGS.get(model_type, {'base_url': '', 'model': '', 'api_key': ''}).copy()

def save_model_config(model_type, base_url, model_name, api_key=''):
    """保存模型完整配置（包括API密钥）"""
    ensure_config_dir()
    config_file = os.path.join(CONFIG_DIR, f'{model_type}_config.json')
    
    # 如果没有提供api_key，保留现有的api_key
    if not api_key:
        existing_config = load_model_config(model_type)
        api_key = existing_config.get('api_key', '')
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump({
                'base_url': base_url,
                'model': model_name,
                'api_key': api_key
            }, f, indent=2, ensure_ascii=False)
        logger.info(f'{model_type}配置已保存')
    except Exception as e:
        logger.error(f'保存{model_type}配置失败: {e}')

def load_api_key(key_type):
    """加载API密钥（从统一配置文件中）"""
    config = load_model_config(key_type)
    return config.get('api_key', '')

def save_api_key(key_type, api_key):
    """保存API密钥（到统一配置文件中）"""
    config = load_model_config(key_type)
    save_model_config(key_type, config.get('base_url', ''), config.get('model', ''), api_key)

# 项目配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# B站API配置
API_CONFIG = {
    'appkey': '783bbb7264451d82',
    'appsec': '2653583c8873dea268ab9386918b1d65',
    'user_agent': 'Mozilla/5.0 BiliDroid/1.12.0 (bbcallen@gmail.com)',
}

HEADERS = {
    'User-Agent': API_CONFIG['user_agent'],
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'x-bili-metadata-legal-region': 'CN',
    'x-bili-aurora-eid': '',
    'x-bili-aurora-zone': '',
}

AUTH_FILE = os.path.join(CONFIG_DIR, 'auth.json')

# LLM提示词模板
PROMPT = '''
当前时间：{}
你是一个高效精准的答题专家，面对选择题时，直接根据问题和选项判断正确答案，并返回对应选项的序号（1, 2, 3, 4）。示例：
问题：大的反义词是什么？
选项：['长', '宽', '小', '热']
回答：3
如果不确定正确答案，选择最接近的选项序号返回，不提供额外解释或超出 1-4 的内容。
---
请回答我的问题：{}
'''

# GUI模式全局变量
model_choice = '1'  # 默认DeepSeek

# 初始化配置
ensure_config_dir()