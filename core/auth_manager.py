#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
认证管理器
统一管理用户登录、登出和账号切换
"""

from PyQt6.QtCore import QObject, pyqtSignal
from scripts.login import auth, is_login, logout


class AuthManager(QObject):
    """认证管理器"""
    
    login_status_changed = pyqtSignal(bool)  # 登录状态变化信号
    
    def __init__(self):
        super().__init__()
        self._logged_in = False
        self.refresh_login_status()
    
    @property
    def is_logged_in(self):
        """是否已登录"""
        return self._logged_in
    
    def refresh_login_status(self):
        """刷新登录状态"""
        new_status = is_login()
        if new_status != self._logged_in:
            self._logged_in = new_status
            self.login_status_changed.emit(new_status)
        return new_status
    
    def login(self, gui_callback=None):
        """登录B站账号
        
        Args:
            gui_callback: GUI回调函数，用于显示二维码
            
        Returns:
            bool: 登录是否成功
        """
        try:
            result = auth(gui_mode=True, gui_callback=gui_callback)
            self.refresh_login_status()
            return result
        except Exception as e:
            from tools.logger import logger
            logger.error(f"登录过程出错: {str(e)}")
            return False
    
    def logout(self):
        """登出当前账号
        
        Returns:
            bool: 登出是否成功
        """
        try:
            result = logout()
            if result:
                self.refresh_login_status()
            return result
        except Exception as e:
            from tools.logger import logger
            logger.error(f"登出过程出错: {str(e)}")
            return False
    
    def switch_account(self, gui_callback=None):
        """切换账号
        
        Args:
            gui_callback: GUI回调函数，用于显示二维码
            
        Returns:
            bool: 切换是否成功
        """
        try:
            # 先登出当前账号
            logout_result = self.logout()
            if not logout_result:
                return False
            
            # 重新登录
            login_result = self.login(gui_callback)
            return login_result
            
        except Exception as e:
            from tools.logger import logger
            logger.error(f"切换账号过程出错: {str(e)}")
            return False
    
    def get_user_info(self):
        """获取当前用户信息
        
        Returns:
            dict: 用户信息，如果未登录则返回None
        """
        if not self.is_logged_in:
            return None
        
        # TODO: 实现获取用户信息的逻辑
        # 这里可以调用B站API获取用户基本信息
        return {
            'logged_in': True,
            'username': '用户',  # 实际应该从API获取
        }
    
    def check_login_validity(self):
        """检查登录有效性
        
        Returns:
            bool: 登录是否仍然有效
        """
        # 定期检查登录状态是否还有效
        # 这对于长时间运行的应用很有用
        return self.refresh_login_status() 