"""
Core module
提供应用程序的核心功能和抽象层
"""

from .app_controller import AppController
from .model_manager import ModelManager
from .auth_manager import AuthManager

__all__ = [
    'AppController',
    'ModelManager', 
    'AuthManager'
] 