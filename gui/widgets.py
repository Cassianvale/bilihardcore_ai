#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QTextEdit, 
                             QFrame, QStackedWidget, QMessageBox, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QTextCursor
from config.config import (load_api_key, save_api_key, load_model_config, 
                          save_model_config)


class LogWidget(QWidget):
    """日志显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 日志框架 - 使用GroupBox
        log_group = QGroupBox("📋 答题日志")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(15, 15, 15, 15)
        log_layout.setSpacing(10)
        
        # 日志操作栏
        log_toolbar = QHBoxLayout()
        
        # 状态指示器
        self.status_indicator = QLabel("🟢 就绪")
        self.status_indicator.setObjectName("statusIndicator")
        
        log_toolbar.addWidget(self.status_indicator)
        log_toolbar.addStretch()
        
        # 清空日志按钮
        clear_btn = QPushButton("🗑️ 清空日志")
        clear_btn.setMaximumWidth(150)
        clear_btn.clicked.connect(self.clear_log)
        log_toolbar.addWidget(clear_btn)
        
        log_layout.addLayout(log_toolbar)
        
        # 日志文本区域
        self.log_text = QTextEdit()
        self.log_text.setObjectName("log_text")  # 设置对象名以应用特定样式
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        self.log_text.setPlaceholderText("日志信息将在这里显示...")
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group)
    
    def append_log(self, text):
        """添加日志"""
        # 根据日志内容更新状态指示器
        if "开始" in text:
            self.status_indicator.setText("🔵 运行中")
        elif "成功" in text or "完成" in text:
            self.status_indicator.setText("🟢 完成")
        elif "失败" in text or "错误" in text:
            self.status_indicator.setText("🔴 错误")
        elif "停止" in text:
            self.status_indicator.setText("🟡 已停止")
        
        # 添加时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}"
        
        self.log_text.append(formatted_text)
        # 自动滚动到底部
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.status_indicator.setText("🟢 就绪")
    
    def set_status(self, status_text):
        """设置状态指示器"""
        self.status_indicator.setText(status_text)


class StatusWidget(QWidget):
    """状态显示组件"""
    
    login_clicked = pyqtSignal()
    logout_clicked = pyqtSignal()
    switch_account_clicked = pyqtSignal()
    start_quiz_clicked = pyqtSignal()
    stop_quiz_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_logged_in = False
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 状态框架 - 使用GroupBox获得更好的视觉效果
        status_group = QGroupBox("💠 答题助手")
        status_layout = QVBoxLayout(status_group)
        
        # 状态信息布局
        status_info_row = QHBoxLayout()
        
        # 状态图标和文本容器
        status_info_layout = QVBoxLayout()
        
        # 登录状态标签
        self.login_status_label = QLabel("登录状态：未登录")
        self.login_status_label.setObjectName("statusLabel")
        
        # 状态提示
        self.status_hint_label = QLabel("💡 请先登录B站账号以开始答题")
        self.status_hint_label.setObjectName("statusHint")
        
        status_info_layout.addWidget(self.login_status_label)
        status_info_layout.addWidget(self.status_hint_label)
        
        # 登录按钮容器
        login_button_layout = QVBoxLayout()
        login_button_layout.setSpacing(8)
        
        # 登录/退出按钮
        self.login_button = QPushButton("登录B站")
        self.login_button.setMinimumHeight(35)
        self.login_button.clicked.connect(self._handle_login_button_click)
        
        # 切换账号按钮
        self.switch_account_button = QPushButton("切换账号")
        self.switch_account_button.setMinimumHeight(35)
        self.switch_account_button.clicked.connect(self.switch_account_clicked.emit)
        
        login_button_layout.addWidget(self.login_button)
        login_button_layout.addWidget(self.switch_account_button)
        
        status_info_row.addLayout(status_info_layout)
        status_info_row.addStretch()
        status_info_row.addLayout(login_button_layout)
        
        status_layout.addLayout(status_info_row)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("separator")
        status_layout.addWidget(separator)
        
        # 答题控制按钮
        quiz_control_layout = QHBoxLayout()
        quiz_control_layout.setSpacing(10)
        
        # 提示信息
        info_label = QLabel("🤖 请确保已在设置中配置好AI模型后再开始答题")
        info_label.setObjectName("controlHint")
        info_label.setWordWrap(True)
        
        # 答题控制按钮
        self.start_button = QPushButton("🚀 开始答题")
        self.start_button.setMinimumHeight(45)
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self.start_quiz_clicked.emit)
        
        self.stop_button = QPushButton("⏹️ 停止答题")
        self.stop_button.setMinimumHeight(45)
        self.stop_button.setObjectName("dangerButton")
        self.stop_button.clicked.connect(self.stop_quiz_clicked.emit)
        
        quiz_control_layout.addWidget(self.start_button)
        quiz_control_layout.addWidget(self.stop_button)
        
        status_layout.addWidget(info_label)
        status_layout.addLayout(quiz_control_layout)
        
        main_layout.addWidget(status_group)
    
    def _handle_login_button_click(self):
        """处理登录/退出按钮点击"""
        if self.is_logged_in:
            self.logout_clicked.emit()
        else:
            self.login_clicked.emit()
    
    def set_login_status(self, is_logged_in):
        """设置登录状态"""
        self.is_logged_in = is_logged_in
        if is_logged_in:
            self.login_status_label.setText("登录状态：✅ 已登录")
            self.status_hint_label.setText("🎉 您已成功登录，可以开始答题了")
            self.login_button.setText("退出登录")
            self.switch_account_button.setEnabled(True)
        else:
            self.login_status_label.setText("登录状态：❌ 未登录")
            self.status_hint_label.setText("💡 请先登录B站账号以开始答题")
            self.login_button.setText("登录B站")
            self.switch_account_button.setEnabled(False)
    
    def set_start_button_enabled(self, enabled):
        """设置开始按钮启用状态"""
        self.start_button.setEnabled(enabled)





class ModelConfigWidget(QWidget):
    """模型配置组件"""
    
    def __init__(self, model_type, parent=None):
        super().__init__(parent)
        self.model_type = model_type
        self.initUI()
        self.load_settings()
    
    def initUI(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 根据模型类型设置标题
        model_titles = {
            "deepseek": "🧠 DeepSeek",
            "gemini": "✨ Gemini", 
            "custom": "⚙️ 自定义模型"
        }
        
        # 添加模型类型标题
        title_label = QLabel(model_titles.get(self.model_type, "模型配置"))
        title_label.setStyleSheet("font-size: 12pt; font-weight: 600; color: #34495e; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        form_layout = QFormLayout()

        # API Key输入
        api_key_label = QLabel(f"API Key: <span style='color: red;'>*</span>")
        api_key_label.setTextFormat(Qt.TextFormat.RichText)
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setPlaceholderText("请输入API Key（必填）")
        form_layout.addRow(api_key_label, self.key_input)
        
        # 获取密钥链接 - 添加为单独的行
        self.get_key_link = QLabel()
        self.get_key_link.setTextFormat(Qt.TextFormat.RichText)
        self.get_key_link.setOpenExternalLinks(True)
        self.get_key_link.setStyleSheet("font-size: 9pt; color: #3498db; margin-top: 3px; margin-left: 5px;")
        form_layout.addRow("", self.get_key_link)

        # API 基础URL输入
        base_url_label = QLabel("API Base URL: <span style='color: red;'>*</span>")
        base_url_label.setTextFormat(Qt.TextFormat.RichText)
        self.url_input = QLineEdit()
        form_layout.addRow(base_url_label, self.url_input)

        # 模型名称输入
        model_name_label = QLabel("模型名称: <span style='color: red;'>*</span>")
        model_name_label.setTextFormat(Qt.TextFormat.RichText)
        self.model_input = QLineEdit()
        form_layout.addRow(model_name_label, self.model_input)
        
        # 根据模型类型设置不同的占位符文本
        self._set_placeholders()

        main_layout.addLayout(form_layout)

        # 保存按钮
        self.save_btn = QPushButton(f"保存模型配置")
        self.save_btn.setObjectName("successButton")  # 应用成功按钮样式
        self.save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # 为自定义模型添加提示
        if self.model_type == "custom":
            tips_label = QLabel("💡请避免使用思考模型！\n例如：硅基流动\nAPI Base URL: https://api.siliconflow.cn\n模型: Qwen/Qwen2.5-32B-Instruct, Qwen/Qwen3-30B-A3B 或 deepseek-ai/DeepSeek-V3")
            tips_label.setStyleSheet("background-color: #e8f4fd; color: #1f5582; padding: 10px; border-radius: 5px; margin-top: 10px; border: 1px solid #b8daff;")
            main_layout.addWidget(tips_label)
        
        main_layout.addStretch()
    
    def _set_placeholders(self):
        """根据模型类型设置占位符文本和获取密钥链接"""
        if self.model_type == "deepseek":
            self.url_input.setPlaceholderText("例如：https://api.deepseek.com（必填）")
            self.model_input.setPlaceholderText("例如：deepseek-chat（必填）")
            self.get_key_link.setText("🔗 <a href='https://platform.deepseek.com/api_keys'>点这里获取DeepSeek API密钥</a>")
        elif self.model_type == "gemini":
            self.url_input.setPlaceholderText("例如：https://generativelanguage.googleapis.com（必填）")
            self.model_input.setPlaceholderText("例如：gemini-2.0-flash（必填）")
            self.get_key_link.setText("🔗 <a href='https://aistudio.google.com/app/apikey'>点这里获取Gemini API密钥</a>")
        elif self.model_type == "custom":
            self.url_input.setPlaceholderText("例如：https://api.siliconflow.cn（必填）")
            self.model_input.setPlaceholderText("例如：deepseek-ai/DeepSeek-V3（必填）")
            self.get_key_link.setText("💡 请根据您选择的API提供商获取相应的密钥")
    
    def load_settings(self):
        """加载设置"""
        config = load_model_config(self.model_type)
        api_key = load_api_key(self.model_type)
        
        self.url_input.setText(config['base_url'])
        self.model_input.setText(config['model'])
        self.key_input.setText(api_key)
    
    def save_settings(self):
        """保存设置"""
        api_key = self.key_input.text().strip()
        base_url = self.url_input.text().strip()
        model_name = self.model_input.text().strip()
        
        # 验证必填字段
        missing_fields = []
        if not api_key:
            missing_fields.append("API Key")
        if not base_url:
            missing_fields.append("API 基础URL")
        if not model_name:
            missing_fields.append("模型名称")
        
        # 如果有缺失字段，显示错误提示
        if missing_fields:
            missing_text = "、".join(missing_fields)
            QMessageBox.warning(
                self, 
                "保存失败", 
                f"请填写完整以下必填字段：\n{missing_text}\n\n所有字段都必须填写才能保存设置。"
            )
            return
        
        # 验证URL格式（基本验证）
        if not base_url.startswith(('http://', 'https://')):
            QMessageBox.warning(
                self,
                "保存失败",
                "API 基础URL格式不正确，请输入完整的URL（以http://或https://开头）"
            )
            return
        
        # 验证API Key长度（基本验证）
        if len(api_key) < 10:
            QMessageBox.warning(
                self,
                "保存失败", 
                "API Key长度过短，请检查API Key是否正确"
            )
            return
        
        try:
            # 保存API密钥
            save_api_key(self.model_type, api_key)
            
            # 保存模型配置
            save_model_config(self.model_type, base_url, model_name)
                
            # 更新全局变量，特别是自定义模型配置
            if self.model_type == "custom":
                import config.config
                config.config.CUSTOM_MODEL_CONFIG = {
                    'base_url': base_url,
                    'model': model_name
                }
                config.config.API_KEY_CUSTOM = api_key
            
            QMessageBox.information(self, "保存成功", f"{self.model_type.upper()} 设置已保存")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "保存失败",
                f"保存设置时出现错误：\n{str(e)}\n\n请检查配置是否正确"
            )
    
    def get_api_key(self):
        """获取API密钥"""
        return self.key_input.text().strip()


class SettingsWidget(QWidget):
    """设置页面组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_model_type = "deepseek"  # 默认模型
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 模型选择区域
        self._setup_model_selection(layout)
        
        # 模型配置区域
        self._setup_model_config(layout)
    
    def _setup_model_selection(self, layout):
        """设置模型选择区域"""
        model_group_box = QGroupBox("选择AI模型")
        model_group_layout = QVBoxLayout(model_group_box)
        
        self.model_combo = QComboBox()
        self.model_combo.setFixedHeight(30)
        self.model_combo.addItem("🧠 DeepSeek", "deepseek")
        self.model_combo.addItem("✨ Gemini", "gemini")
        self.model_combo.addItem("⚙️ 自定义模型", "custom")
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        
        model_group_layout.addWidget(self.model_combo)
        layout.addWidget(model_group_box)
    
    def _setup_model_config(self, layout):
        """设置模型配置区域"""
        # 创建模型配置组框，与模型选择区域保持一致的边框样式
        config_group_box = QGroupBox("模型配置")
        config_group_layout = QVBoxLayout(config_group_box)
        
        # 模型配置堆叠部件
        self.model_stack = QStackedWidget()
        
        # DeepSeek配置
        self.deepseek_widget = ModelConfigWidget("deepseek")
        self.model_stack.addWidget(self.deepseek_widget)
        
        # Gemini配置
        self.gemini_widget = ModelConfigWidget("gemini")
        self.model_stack.addWidget(self.gemini_widget)
        
        # 自定义模型配置
        self.custom_widget = ModelConfigWidget("custom")
        self.model_stack.addWidget(self.custom_widget)
        
        config_group_layout.addWidget(self.model_stack)
        layout.addWidget(config_group_box)
    
    def on_model_changed(self, index):
        """模型选择改变时的回调"""
        model_data = self.model_combo.itemData(index)
        self.current_model_type = model_data
        self.model_stack.setCurrentIndex(index)
    
    def get_current_model_info(self):
        """获取当前模型信息"""
        if self.current_model_type == "deepseek":
            api_key = self.deepseek_widget.get_api_key()
            model_choice_value = "1"
        elif self.current_model_type == "gemini":
            api_key = self.gemini_widget.get_api_key()
            model_choice_value = "2"
        elif self.current_model_type == "custom":
            api_key = self.custom_widget.get_api_key()
            model_choice_value = "3"
        else:
            api_key = ""
            model_choice_value = "1"
        
        return {
            'type': self.current_model_type,
            'api_key': api_key,
            'choice_value': model_choice_value
        }


class AboutWidget(QWidget):
    """关于页面组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <h2 style="text-align: center;">B站答题助手</h2>
        <p style="text-align: center;">一个帮助B站用户自动完成答题任务的工具</p>
        <p><b>功能特点:</b></p>
        <ul>
            <li>支持使用多种AI模型</li>
            <li>支持DeepSeek、Gemini和自定义模型</li>
            <li>支持阿里云通义千问等API</li>
            <li>现代化GUI界面</li>
        </ul>
        <p><b>使用说明:</b></p>
        <ol>
            <li>在"设置"标签页配置API密钥和模型</li>
            <li>在"首页"登录B站账号</li>
            <li>点击"开始答题"按钮开始自动答题</li>
        </ol>
        <p><b>注意事项:</b></p>
        <ul>
            <li>使用前请确保已配置正确的API密钥</li>
            <li>程序仅调用B站接口和LLM API，不会上传个人信息</li>
            <li>如果使用Gemini，注意需要切换至Gemini允许的地区运行</li>
        </ul>
        """)
        
        layout.addWidget(about_text) 