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
    
    # 获取目标架构（来自环境变量或默认值）
    target_arch = os.environ.get('PYINSTALLER_TARGET_ARCH', None)
    if system == 'darwin' and target_arch:
        # 确保macOS使用正确的架构名称
        if target_arch == 'x64':
            target_arch = 'x86_64'
    elif system != 'darwin':
        # 非macOS平台不需要target_arch
        target_arch = None
    
    # 获取控制台模式设置
    console_build = os.environ.get('CONSOLE_BUILD', 'false').lower() == 'true'
    
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
    
    # 使用安全的路径字符串（避免__file__问题）
    safe_current_dir = str(current_dir).replace('\\', '/')
    safe_entry_point = str(entry_point).replace('\\', '/')
    
    # 生成macOS bundle部分
    if system == "darwin":
        bundle_part = f'''
app = BUNDLE(
    coll,
    name='BiliHardcore_AI.app',{f"""
    icon=r'{icon_path}',""" if icon_path else ""}
    bundle_identifier='com.github.bilihardcore.ai',
    info_plist={{
        'CFBundleDisplayName': 'B站硬核会员自动答题工具',
        'CFBundleIdentifier': 'com.github.bilihardcore.ai',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    }},
)'''
    else:
        bundle_part = '''
# macOS Bundle (not needed on this platform)
# app = BUNDLE(
#     coll,
#     name='BiliHardcore_AI.app',
#     icon=None,
#     bundle_identifier=None,
#     info_plist={},
# )'''

    # 生成spec文件内容
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# 自动生成的PyInstaller spec文件
# 生成时间: {__import__('datetime').datetime.now().isoformat()}
# 平台: {platform.platform()}

import os
from pathlib import Path

# 获取当前目录 (使用绝对路径避免__file__问题)
current_dir = Path(r"{safe_current_dir}")

block_cipher = None

a = Analysis(
    [r"{safe_entry_point}"],
    pathex=[r"{safe_current_dir}"],
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
    console={str(console_build)},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch={repr(target_arch) if target_arch else 'None'},
    codesign_identity=None,
    entitlements_file=None,{f"""
    icon=r'{icon_path}',""" if icon_path else ""}
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BiliHardcore_AI',
){bundle_part}
'''

    # 写入spec文件
    spec_file = current_dir / "BiliHardcore_AI.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"[OK] Spec file generated: {spec_file}")
    print(f"[INFO] Current directory: {current_dir}")
    print(f"[INFO] Entry point: {entry_point}")
    print(f"[INFO] Icon file: {icon_path or 'Not found'}")
    print(f"[INFO] Data directories: {len(datas)} found")
    print(f"[INFO] Target platform: {system}")
    print(f"[INFO] Target architecture: {target_arch or 'Default'}")
    print(f"[INFO] Console mode: {console_build}")
    
    return str(spec_file)

if __name__ == "__main__":
    create_spec_file() 