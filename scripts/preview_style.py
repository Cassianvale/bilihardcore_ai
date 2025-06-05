#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样式预览脚本 - 用于展示GUI样式优化效果"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from gui.widgets import SettingsWidget, LogWidget, StatusWidget, ControlWidget, AboutWidget
from gui.style import STYLE_SHEET


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 应用样式表
    app.setStyleSheet(STYLE_SHEET)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("B站答题助手 - 样式预览")
    window.resize(800, 600)
    
    # 创建标签页
    tabs = QTabWidget()
    
    # 创建首页（包含多个组件）
    home_widget = QWidget()
    home_layout = QVBoxLayout(home_widget)
    
    # 添加状态组件
    status_widget = StatusWidget()
    home_layout.addWidget(status_widget)
    
    # 添加控制组件
    control_widget = ControlWidget()
    home_layout.addWidget(control_widget)
    
    # 添加日志组件
    log_widget = LogWidget()
    log_widget.append_log("✅ 程序启动成功")
    log_widget.append_log("🎨 新样式已应用")
    log_widget.append_log("📝 这是一个日志示例")
    home_layout.addWidget(log_widget)
    
    # 添加标签页
    tabs.addTab(home_widget, "首页")
    tabs.addTab(SettingsWidget(), "设置")
    tabs.addTab(AboutWidget(), "关于")
    
    window.setCentralWidget(tabs)
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main() 