#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模型管理器
统一管理AI模型的配置、验证和切换
"""

from PyQt6.QtCore import QObject, pyqtSignal
from config.config import (load_api_key, save_api_key, load_model_config, 
                          save_model_config)


class ModelManager(QObject):
    """模型管理器"""
    
    model_changed = pyqtSignal(str)  # 模型切换信号
    
    AVAILABLE_MODELS = {
        'deepseek': {
            'name': 'DeepSeek',
            'choice_value': '1',
            'default_config': {
                'base_url': 'https://api.deepseek.com',
                'model': 'deepseek-chat'
            }
        },
        'gemini': {
            'name': 'Gemini',
            'choice_value': '2',
            'default_config': {
                'base_url': 'https://generativelanguage.googleapis.com',
                'model': 'gemini-pro'
            }
        },
        'custom': {
            'name': '自定义模型',
            'choice_value': '3',
            'default_config': {
                'base_url': 'https://dashscope.aliyuncs.com',
                'model': 'qwen-turbo'
            }
        }
    }
    
    def __init__(self):
        super().__init__()
        self.current_model = 'deepseek'  # 默认模型
    
    def get_available_models(self):
        """获取可用模型列表"""
        return list(self.AVAILABLE_MODELS.keys())
    
    def get_model_display_name(self, model_type):
        """获取模型显示名称"""
        return self.AVAILABLE_MODELS.get(model_type, {}).get('name', model_type)
    
    def set_current_model(self, model_type):
        """设置当前模型"""
        if model_type in self.AVAILABLE_MODELS:
            old_model = self.current_model
            self.current_model = model_type
            if old_model != model_type:
                self.model_changed.emit(model_type)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")
    
    def get_current_model_info(self):
        """获取当前模型信息"""
        model_info = self.AVAILABLE_MODELS.get(self.current_model, {})
        config = load_model_config(self.current_model)
        api_key = load_api_key(self.current_model)
        
        return {
            'type': self.current_model,
            'name': model_info.get('name', self.current_model),
            'choice_value': model_info.get('choice_value', '1'),
            'api_key': api_key,
            'base_url': config.get('base_url', ''),
            'model': config.get('model', ''),
            'config': config
        }
    
    def save_model_config(self, model_type, api_key, base_url, model_name):
        """保存模型配置"""
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"不支持的模型类型: {model_type}")
        
        # 保存API密钥
        if api_key:
            save_api_key(model_type, api_key)
        
        # 保存模型配置
        if base_url and model_name:
            save_model_config(model_type, base_url, model_name)
        
        # 更新全局变量，特别是自定义模型配置
        if model_type == "custom":
            import config.config
            config.config.CUSTOM_MODEL_CONFIG = {
                'base_url': base_url,
                'model': model_name
            }
            config.config.API_KEY_CUSTOM = api_key
    
    def validate_current_model(self):
        """验证当前模型配置"""
        info = self.get_current_model_info()
        
        errors = []
        
        if not info['api_key']:
            errors.append(f"{info['name']} API密钥未配置")
        
        if not info['base_url']:
            errors.append(f"{info['name']} API基础URL未配置")
        
        if not info['model']:
            errors.append(f"{info['name']} 模型名称未配置")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'info': info
        }
    
    def get_model_config(self, model_type):
        """获取指定模型的配置"""
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"不支持的模型类型: {model_type}")
        
        config = load_model_config(model_type)
        api_key = load_api_key(model_type)
        model_info = self.AVAILABLE_MODELS[model_type]
        
        return {
            'type': model_type,
            'name': model_info['name'],
            'choice_value': model_info['choice_value'],
            'api_key': api_key,
            'base_url': config.get('base_url', ''),
            'model': config.get('model', ''),
            'default_config': model_info.get('default_config', {})
        }
    
    def reset_model_config(self, model_type):
        """重置模型配置为默认值"""
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"不支持的模型类型: {model_type}")
        
        default_config = self.AVAILABLE_MODELS[model_type].get('default_config', {})
        
        if default_config:
            save_model_config(
                model_type, 
                default_config.get('base_url', ''),
                default_config.get('model', '')
            ) 