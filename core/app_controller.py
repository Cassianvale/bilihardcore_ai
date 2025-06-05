#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
应用程序控制器
统一管理应用的核心逻辑和状态
"""

from PyQt6.QtCore import QObject, pyqtSignal
from .model_manager import ModelManager
from .auth_manager import AuthManager
from scripts.start_senior import QuizSession


class AppController(QObject):
    """应用程序控制器"""
    
    # 信号定义
    login_status_changed = pyqtSignal(bool)
    model_changed = pyqtSignal(str)
    quiz_status_changed = pyqtSignal(bool)
    log_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager()
        self.auth_manager = AuthManager()
        self.quiz_session = None
        self._setup_connections()
    
    def _setup_connections(self):
        """设置内部信号连接"""
        self.auth_manager.login_status_changed.connect(self.login_status_changed.emit)
        self.model_manager.model_changed.connect(self.model_changed.emit)
    
    @property
    def is_logged_in(self):
        """是否已登录"""
        return self.auth_manager.is_logged_in
    
    @property
    def current_model_info(self):
        """当前模型信息"""
        return self.model_manager.get_current_model_info()
    
    def login(self, gui_callback=None):
        """登录"""
        return self.auth_manager.login(gui_callback)
    
    def logout(self):
        """登出"""
        return self.auth_manager.logout()
    
    def switch_account(self, gui_callback=None):
        """切换账号"""
        return self.auth_manager.switch_account(gui_callback)
    
    def set_model(self, model_type):
        """设置模型"""
        self.model_manager.set_current_model(model_type)
    
    def save_model_config(self, model_type, api_key, base_url, model_name):
        """保存模型配置"""
        self.model_manager.save_model_config(model_type, api_key, base_url, model_name)
    
    def start_quiz(self):
        """开始答题"""
        if not self.is_logged_in:
            raise RuntimeError("请先登录B站账号")
        
        model_info = self.current_model_info
        if not model_info['api_key']:
            raise RuntimeError(f"请先配置{model_info['type'].upper()} API密钥")
        
        # 创建答题会话
        self.quiz_session = QuizSession()
        self.quiz_session.update_model_choice(model_info['choice_value'])
        
        # 设置全局模型选择
        import config.config
        config.config.model_choice = model_info['choice_value']
        
        self.quiz_status_changed.emit(True)
        self.log_message.emit(f"开始使用 {model_info['type'].upper()} 模型答题...")
        
        return self.quiz_session
    
    def stop_quiz(self):
        """停止答题"""
        if self.quiz_session:
            self.quiz_session.stopped = True
            self.quiz_session = None
        
        self.quiz_status_changed.emit(False)
        self.log_message.emit("答题已停止")
    
    def get_model_list(self):
        """获取可用模型列表"""
        return self.model_manager.get_available_models()
    
    def validate_current_model(self):
        """验证当前模型配置"""
        return self.model_manager.validate_current_model() 