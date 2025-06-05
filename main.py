#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main():
    """主函数，启动GUI应用"""
    try:
        from gui.main_window import main as _main
        _main()
    except ImportError as e:
        error_msg = f"错误: 无法导入GUI模块: {e}\n请确保已安装必要的依赖: pip install PySide6"
        print(error_msg)
        
        # 尝试创建错误日志
        try:
            log_path = os.path.join(current_dir, "logs")
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            
            with open(os.path.join(log_path, "gui_error.log"), "w", encoding="utf-8") as f:
                f.write(f"GUI启动错误: {error_msg}\n")
        except:
            pass  # 忽略日志写入错误
        
        # 尝试显示图形化错误消息
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "启动错误", error_msg)
        except:
            pass  # 如果PySide6也无法导入，只显示控制台错误
        
        sys.exit(1)
    except Exception as e:
        error_msg = f"程序启动失败: {str(e)}"
        print(error_msg)
        
        # 记录错误日志
        try:
            log_path = os.path.join(current_dir, "logs")
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            
            with open(os.path.join(log_path, "gui_error.log"), "w", encoding="utf-8") as f:
                f.write(f"程序启动错误: {error_msg}\n")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main() 