#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from loguru import logger as loguru_logger

def setup_logger(name='hardcore-freedom'):
    """设置日志系统
    
    Args:
        name (str): 日志器名称
    
    Returns:
        loguru.Logger: 配置好的日志器实例
    """
    # 移除默认的处理器
    loguru_logger.remove()
    
    # 创建日志目录
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的环境
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境
        base_dir = os.path.dirname(os.path.dirname(__file__))
    
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 设置日志文件路径
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
    
    # 添加控制台处理器（只在有控制台时）
    if sys.stdout is not None:
        loguru_logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
            colorize=True
        )
    
    # 添加文件处理器
    loguru_logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="10 MB",  # 文件大小达到10MB时轮转
        retention="30 days",  # 保留30天的日志
        compression="zip",  # 压缩旧日志文件
        encoding="utf-8"
    )
    
    # 配置日志器名称
    loguru_logger.configure(extra={"name": name})
    
    return loguru_logger

# 创建全局日志器实例
logger = setup_logger()