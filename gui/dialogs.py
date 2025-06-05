#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qrcode
from io import BytesIO
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QFormLayout, 
                             QDialogButtonBox)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QPixmap


class QRCodeDialog(QDialog):
    """二维码登录对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = None
        self.login_result = False
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle("B站扫码登录")
        self.setMinimumSize(300, 400)
        
        layout = QVBoxLayout(self)
        
        # 提示文本
        hint_label = QLabel("请使用哔哩哔哩APP扫描二维码登录")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_label)
        
        # 二维码图像
        self.qrcode_label = QLabel()
        self.qrcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qrcode_label.setMinimumSize(200, 200)
        layout.addWidget(self.qrcode_label)
        
        # 状态提示
        self.status_label = QLabel("等待扫码...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)
    
    def set_qr_code(self, url):
        """设置二维码图像"""
        self.url = url
        
        try:
            # 生成二维码图像
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=2,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # 创建图像
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 将PIL图像转换为QPixmap
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            # 缩放图像到合适的大小
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
            
            # 显示二维码
            self.qrcode_label.setPixmap(pixmap)
            
            # 以文本方式也显示链接
            self.status_label.setText(f"<a href='{url}'>如果二维码无法显示，点击这里打开链接</a>")
            self.status_label.setOpenExternalLinks(True)
        except Exception as e:
            self.status_label.setText(f"生成二维码失败: {e}")
    
    def set_status(self, status):
        """设置状态提示文本"""
        self.status_label.setText(status)
    
    def set_login_result(self, success):
        """设置登录结果"""
        self.login_result = success
        if success:
            self.set_status("登录成功！")
            self.accept()
        else:
            self.set_status("登录失败，请重试")


class CaptchaDialog(QDialog):
    """验证码输入对话框"""
    
    def __init__(self, url=None, categories=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.categories = categories
        self.captcha_text = ""
        self.category_ids = ""
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle("验证码")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 显示分类信息
        if self.categories:
            self._setup_categories_section(layout)
        
        # 显示验证码图片
        if self.url:
            self._setup_captcha_image_section(layout)
        
        # 验证码输入
        self._setup_captcha_input_section(layout)
        
        # 按钮
        self._setup_buttons(layout)
    
    def _setup_categories_section(self, layout):
        """设置分类选择区域"""
        cats_label = QLabel("请选择以下分类ID:")
        layout.addWidget(cats_label)
        
        cats_text = QTextEdit()
        cats_text.setReadOnly(True)
        cats_text.setMaximumHeight(120)
        
        cats_info = ""
        for cat in self.categories:
            cats_info += f"ID: {cat.get('id')} - {cat.get('name')}\n"
        cats_text.setText(cats_info)
        layout.addWidget(cats_text)
        
        id_label = QLabel("输入分类ID (多个ID用英文逗号隔开):")
        layout.addWidget(id_label)
        
        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)
    
    def _setup_captcha_image_section(self, layout):
        """设置验证码图片区域"""
        # 添加验证码图片标签
        self.captcha_img_label = QLabel("加载验证码中...")
        self.captcha_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.captcha_img_label.setMinimumHeight(100)
        layout.addWidget(self.captcha_img_label)
        
        # 加载验证码图片
        self.load_captcha_image()
        
        # 同时提供链接作为备用
        url_label = QLabel(f"验证码链接: <a href='{self.url}'>{self.url}</a>")
        url_label.setOpenExternalLinks(True)
        layout.addWidget(url_label)
    
    def _setup_captcha_input_section(self, layout):
        """设置验证码输入区域"""
        captcha_label = QLabel("输入验证码:")
        layout.addWidget(captcha_label)
        
        self.captcha_input = QLineEdit()
        layout.addWidget(self.captcha_input)
    
    def _setup_buttons(self, layout):
        """设置按钮区域"""
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                     QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_captcha_image(self):
        """加载验证码图片"""
        try:
            import requests
            
            # 在一个新线程中下载图片
            class ImageDownloader(QThread):
                image_loaded = Signal(bytes)
                
                def __init__(self, url):
                    super().__init__()
                    self.url = url
                
                def run(self):
                    try:
                        response = requests.get(self.url, timeout=10)
                        if response.status_code == 200:
                            self.image_loaded.emit(response.content)
                    except Exception as e:
                        print(f"加载验证码图片出错: {e}")
            
            # 创建下载线程
            self.downloader = ImageDownloader(self.url)
            
            # 连接信号
            self.downloader.image_loaded.connect(self.set_captcha_image)
            
            # 启动线程
            self.downloader.start()
        except Exception as e:
            self.captcha_img_label.setText(f"加载验证码失败: {e}")
    
    def set_captcha_image(self, image_data):
        """设置验证码图片"""
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            
            # 确保图片不会太大
            if pixmap.width() > 400:
                pixmap = pixmap.scaled(400, pixmap.height() * 400 // pixmap.width(), 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
            
            self.captcha_img_label.setPixmap(pixmap)
        except Exception as e:
            self.captcha_img_label.setText(f"显示验证码失败: {e}")
    
    def accept(self):
        """接受对话框输入"""
        if hasattr(self, 'id_input'):
            self.category_ids = self.id_input.text().strip()
        self.captcha_text = self.captcha_input.text().strip()
        super().accept() 