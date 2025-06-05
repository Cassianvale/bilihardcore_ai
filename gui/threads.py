#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from PySide6.QtCore import QThread, Signal
from scripts.start_senior import QuizSession
from scripts.login import auth
from tools.logger import logger


class QuizThread(QThread):
    """答题线程类"""
    
    log_signal = Signal(str)
    finished_signal = Signal()
    captcha_signal = Signal(str, list)
    
    def __init__(self):
        super().__init__()
        self.quiz_session = QuizSession()
        self.stopped = False
        self.captcha_result = None
        self.categories_result = None
        self.captcha_wait_event = threading.Event()
    
    def run(self):
        """线程运行主逻辑"""
        try:
            # 保存原始输入函数
            global input
            original_input_func = input
            
            # 从正确的模块导入函数
            from client.senior import captcha_get, captcha_submit, category_get
            
            # 重写输入函数
            def custom_input(prompt):
                return self._handle_custom_input(prompt, original_input_func)
            
            # 保存原始方法
            original_handle_verification = self.quiz_session.handle_verification
            
            # 重写处理验证过程的方法
            def patched_handle_verification():
                return self._handle_verification_process(category_get, captcha_get, captcha_submit)
            
            # 应用补丁
            input = custom_input
            self.quiz_session.handle_verification = patched_handle_verification
            
            # 应用日志补丁
            self._patch_logger()
            
            # 开始答题
            self.quiz_session.start()
            
        except Exception as e:
            self.log_signal.emit(f"答题过程出错: {str(e)}")
        finally:
            # 恢复原始方法
            input = original_input_func
            self._restore_logger()
            self.quiz_session.handle_verification = original_handle_verification
            self.finished_signal.emit()
    
    def _handle_custom_input(self, prompt, original_input_func):
        """处理自定义输入"""
        if "分类ID" in prompt and hasattr(self, "categories_data"):
            # 重置等待事件
            self.captcha_wait_event.clear()
            # 发出信号请求分类ID
            self.captcha_signal.emit("", self.categories_data)
            # 等待结果
            self.captcha_wait_event.wait(30)  # 最多等待30秒
            if self.stopped:
                return ""
            result = self.categories_result
            self.categories_result = None
            return result if result else ""
        elif "验证码" in prompt and hasattr(self, "captcha_url"):
            # 重置等待事件
            self.captcha_wait_event.clear()
            # 发出信号请求验证码
            self.captcha_signal.emit(self.captcha_url, [])
            # 等待结果
            self.captcha_wait_event.wait(30)  # 最多等待30秒
            if self.stopped:
                return ""
            result = self.captcha_result
            self.captcha_result = None
            return result if result else ""
        else:
            self.log_signal.emit(f"输入提示: {prompt}")
            return original_input_func(prompt)
    
    def _handle_verification_process(self, category_get, captcha_get, captcha_submit):
        """处理验证过程"""
        try:
            if self.quiz_session.stopped:
                self.log_signal.emit("答题已停止")
                return False
            
            self.log_signal.emit("获取分类信息...")
            category_result = category_get()
            if not category_result:
                return False
            
            if self.quiz_session.stopped:
                self.log_signal.emit("答题已停止")
                return False
            
            # 保存分类数据供GUI使用
            self.categories_data = category_result.get('categories', [])
            self.log_signal.emit("显示验证码分类选择对话框...")
            
            # 获取用户输入的分类ID
            ids = self._handle_custom_input('请输入分类ID: ', input)
            
            if self.quiz_session.stopped:
                self.log_signal.emit("答题已停止")
                return False
            
            self.log_signal.emit("获取验证码...")
            captcha_res = captcha_get()
            if not captcha_res:
                return False
            
            # 保存验证码URL供GUI使用
            self.captcha_url = captcha_res.get('url')
            self.log_signal.emit(f"显示验证码输入对话框，验证码链接: {self.captcha_url}")
            
            # 获取用户输入的验证码
            captcha = self._handle_custom_input('请输入验证码: ', input)
            
            if captcha_submit(code=captcha, captcha_token=captcha_res.get('token'), ids=ids):
                self.log_signal.emit("验证通过✅")
                return self.quiz_session.get_question()
            else:
                self.log_signal.emit("验证失败")
                return False
                
        except Exception as e:
            self.log_signal.emit(f"验证过程发生错误: {str(e)}")
            return False
    
    def _patch_logger(self):
        """应用日志补丁"""
        def patched_info(msg, *args, **kwargs):
            self.log_signal.emit(f"INFO: {msg}")
            logger.orig_info(msg, *args, **kwargs)
        
        def patched_error(msg, *args, **kwargs):
            self.log_signal.emit(f"ERROR: {msg}")
            logger.orig_error(msg, *args, **kwargs)
        
        def patched_warning(msg, *args, **kwargs):
            self.log_signal.emit(f"WARNING: {msg}")
            logger.orig_warning(msg, *args, **kwargs)
        
        # 保存原始方法
        if not hasattr(logger, 'orig_info'):
            logger.orig_info = logger.info
            logger.orig_error = logger.error
            logger.orig_warning = logger.warning
        
        # 应用日志补丁
        logger.info = patched_info
        logger.error = patched_error
        logger.warning = patched_warning
    
    def _restore_logger(self):
        """恢复日志方法"""
        if hasattr(logger, 'orig_info'):
            logger.info = logger.orig_info
            logger.error = logger.orig_error
            logger.warning = logger.orig_warning
    
    def stop(self):
        """停止线程"""
        self.stopped = True
        self.quiz_session.stopped = True
        # 防止线程卡在等待输入
        self.captcha_result = ""
        self.categories_result = ""
        self.captcha_wait_event.set()  # 解除等待状态
        self.terminate()
    
    def set_captcha_result(self, captcha_text, category_ids=""):
        """设置验证码结果"""
        self.captcha_result = captcha_text
        if category_ids:
            self.categories_result = category_ids
        # 设置事件，通知等待的线程继续执行
        self.captcha_wait_event.set()


class LoginThread(QThread):
    """登录线程类"""
    
    login_finished = Signal(bool)
    update_qr = Signal(str)
    
    def __init__(self, gui_callback=None):
        super().__init__()
        self.gui_callback = gui_callback
    
    def run(self):
        """线程运行主逻辑"""
        try:
            # 定义GUI回调函数，用于显示二维码
            def show_qrcode(url):
                self.update_qr.emit(url)
            
            # 调用auth函数，使用GUI模式
            result = auth(gui_mode=True, gui_callback=show_qrcode)
            self.login_finished.emit(result)
        except Exception as e:
            logger.error(f"登录出错: {str(e)}")
            self.login_finished.emit(False)


class SwitchAccountThread(QThread):
    """切换账号线程类"""
    
    finished = Signal(bool)
    update_qr = Signal(str)
    logout_signal = Signal(bool)
    
    def run(self):
        """线程运行主逻辑"""
        try:
            from scripts.login import logout
            
            # 先登出当前账号
            logout_result = logout()
            self.logout_signal.emit(logout_result)
            
            if logout_result:
                # 定义GUI回调函数，用于显示二维码
                def show_qrcode(url):
                    self.update_qr.emit(url)
                
                # 调用登录函数
                result = auth(gui_mode=True, gui_callback=show_qrcode)
                self.finished.emit(result)
            else:
                self.finished.emit(False)
        except Exception as e:
            logger.error(f"切换账号过程出错: {str(e)}")
            self.finished.emit(False) 