#!/usr/bin/env python3
"""
动态生成PyInstaller spec文件的脚本
支持跨平台构建，避免硬编码路径
"""

import os
import sys
import platform
from pathlib import Path

def create_spec_file():
    """创建动态的PyInstaller spec文件"""
    
    # 获取当前工作目录
    current_dir = Path.cwd()
    entry_point = current_dir / "run.py"
    
    # 确定平台特定的设置
    system = platform.system().lower()
    
    # 图标文件路径（如果存在）
    icon_path = None
    possible_icons = [
        current_dir / "assets" / "icon.ico",
        current_dir / "assets" / "icon.png",
        current_dir / "assets" / "app.ico",
        current_dir / "icon.ico"
    ]
    
    for icon in possible_icons:
        if icon.exists():
            icon_path = str(icon)
            break
    
    # 数据文件配置
    datas = []
    
    # 检查并添加各种可能的数据目录
    data_dirs = ["config", "assets", "tools", "client"]
    for data_dir in data_dirs:
        dir_path = current_dir / data_dir
        if dir_path.exists():
            if system == "windows":
                datas.append(f"('{data_dir}', '{data_dir}')")
            else:
                datas.append(f"('{data_dir}', '{data_dir}')")
    
    # 隐藏导入配置
    hidden_imports = [
        "'PySide6.QtCore'",
        "'PySide6.QtGui'", 
        "'PySide6.QtWidgets'",
        "'requests'",
        "'qrcode'",
        "'loguru'",
        "'certifi'",
        "'charset_normalizer'",
        "'urllib3'",
        "'PIL'",
        "'PIL.Image'"
    ]
    
    # 生成spec文件内容
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# 自动生成的PyInstaller spec文件
# 生成时间: {__import__('datetime').datetime.now().isoformat()}
# 平台: {platform.platform()}

import os
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['{entry_point}'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[{', '.join(datas) if datas else ''}],
    hiddenimports=[{', '.join(hidden_imports)}],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'test',
        'tests',
        'testing'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 过滤掉不需要的文件
a.datas = [x for x in a.datas if not x[0].startswith('share/')]
a.datas = [x for x in a.datas if not x[0].startswith('lib/python')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BiliHardcore_AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console={"True" if "--console" in sys.argv else "False"},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,{f"""
    icon='{icon_path}',""" if icon_path else ""}
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BiliHardcore_AI',
)

# macOS特定配置
{"app = BUNDLE(" if system == "darwin" else "# app = BUNDLE("}
{"    coll," if system == "darwin" else "    # coll,"}
{"    name='BiliHardcore_AI.app'," if system == "darwin" else "    # name='BiliHardcore_AI.app',"}
{"    icon=icon_path," if system == "darwin" and icon_path else "    # icon=None,"}
{"    bundle_identifier='com.github.bilihardcore.ai'," if system == "darwin" else "    # bundle_identifier=None,"}
{"    info_plist={{" if system == "darwin" else "    # info_plist={"}
{"        'CFBundleDisplayName': 'B站硬核会员自动答题工具'," if system == "darwin" else "        # 'CFBundleDisplayName': 'App Name',"}
{"        'CFBundleIdentifier': 'com.github.bilihardcore.ai'," if system == "darwin" else "        # 'CFBundleIdentifier': 'com.example.app',"}
{"        'CFBundleVersion': '1.0.0'," if system == "darwin" else "        # 'CFBundleVersion': '1.0.0',"}
{"        'CFBundleShortVersionString': '1.0.0'," if system == "darwin" else "        # 'CFBundleShortVersionString': '1.0.0',"}
{"        'NSHighResolutionCapable': True," if system == "darwin" else "        # 'NSHighResolutionCapable': True,"}
{"    }}," if system == "darwin" else "    # },"}
{")" if system == "darwin" else "# )"}
'''

    # 写入spec文件
    spec_file = current_dir / "BiliHardcore_AI.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Spec文件已生成: {spec_file}")
    print(f"📁 当前目录: {current_dir}")
    print(f"🐍 入口文件: {entry_point}")
    print(f"🖼️ 图标文件: {icon_path or '未找到'}")
    print(f"📦 数据目录: {len(datas)} 个")
    print(f"💻 目标平台: {system}")
    
    return str(spec_file)

if __name__ == "__main__":
    create_spec_file() 