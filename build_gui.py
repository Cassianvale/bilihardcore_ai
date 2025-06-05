#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import glob
import zipfile
from pathlib import Path
from datetime import datetime

def clean_python_cache():
    """清理Python缓存文件"""
    print("🧹 开始清理Python缓存...")
    
    current_dir = Path(__file__).parent
    
    # 清理 __pycache__ 文件夹
    pycache_dirs = list(current_dir.rglob("__pycache__"))
    for cache_dir in pycache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"  删除缓存目录: {cache_dir}")
        except Exception as e:
            print(f"  删除缓存目录失败 {cache_dir}: {e}")
    
    # 清理 .pyc 文件
    pyc_files = list(current_dir.rglob("*.pyc"))
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            print(f"  删除缓存文件: {pyc_file}")
        except Exception as e:
            print(f"  删除缓存文件失败 {pyc_file}: {e}")
    
    # 清理 .pyo 文件
    pyo_files = list(current_dir.rglob("*.pyo"))
    for pyo_file in pyo_files:
        try:
            pyo_file.unlink()
            print(f"  删除优化文件: {pyo_file}")
        except Exception as e:
            print(f"  删除优化文件失败 {pyo_file}: {e}")
    
    print("✅ Python缓存清理完成")

def clean_build_dirs():
    """清理构建目录"""
    print("🧹 清理构建目录...")
    
    current_dir = Path(__file__).parent
    build_dirs = ["build", "dist"]
    
    for dir_name in build_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  删除构建目录: {dir_path}")
            except Exception as e:
                print(f"  删除构建目录失败 {dir_path}: {e}")
    
    # 清理 .spec 文件
    spec_files = list(current_dir.glob("*.spec"))
    for spec_file in spec_files:
        try:
            spec_file.unlink()
            print(f"  删除spec文件: {spec_file}")
        except Exception as e:
            print(f"  删除spec文件失败 {spec_file}: {e}")
    
    # 清理旧的ZIP文件
    zip_files = list(current_dir.glob("BiliHardcore_AI_*.zip"))
    for zip_file in zip_files:
        try:
            zip_file.unlink()
            print(f"  删除旧的ZIP文件: {zip_file}")
        except Exception as e:
            print(f"  删除ZIP文件失败 {zip_file}: {e}")
    
    print("✅ 构建目录清理完成")

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")
    
    try:
        import PyInstaller
        print(f"  ✅ PyInstaller已安装: {PyInstaller.__version__}")
    except ImportError:
        print("  ❌ PyInstaller未安装")
        print("  请运行: pip install pyinstaller")
        return False
    
    try:
        import PySide6
        print(f"  ✅ PySide6已安装")
    except ImportError:
        print("  ❌ PySide6未安装")
        print("  请运行: pip install PySide6")
        return False
    
    # 检查主要文件是否存在
    main_file = Path(__file__).parent / "run.py"
    if not main_file.exists():
        print(f"  ❌ 主文件不存在: {main_file}")
        return False
    else:
        print(f"  ✅ 主文件存在: {main_file}")
    
    return True

def build_executable():
    """使用PyInstaller构建可执行文件"""
    print("🔨 开始构建可执行文件...")
    
    current_dir = Path(__file__).parent
    main_script = current_dir / "run.py"
    
    # PyInstaller命令参数
    cmd = [
        "pyinstaller",
        "--windowed",             # Windows GUI应用，不显示控制台窗口
        "--noconfirm",            # 覆盖输出目录而不询问
        "--clean",                # 构建前清理缓存和临时文件
        f"--name=BiliHardcore_AI",      # 可执行文件名称
        str(main_script)
    ]
    
    try:
        # 执行PyInstaller命令
        result = subprocess.run(cmd, check=True, capture_output=False, text=True, encoding='utf-8')
        print("✅ 构建成功！")
        
        # 显示输出文件信息
        dist_dir = current_dir / "dist"
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            if exe_files:
                exe_file = exe_files[0]
                file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
                print(f"📦 可执行文件: {exe_file}")
                print(f"📏 文件大小: {file_size:.1f} MB")
            else:
                print("⚠️  未找到生成的可执行文件")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False

def create_zip_package():
    """将构建的程序打包成zip压缩包"""
    print("📦 开始创建ZIP压缩包...")
    
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    
    if not dist_dir.exists():
        print("❌ dist目录不存在，无法创建压缩包")
        return False
    
    # 创建压缩包文件名（包含时间戳）
    zip_filename = f"BiliHardcore_AI.zip"
    zip_path = current_dir / zip_filename
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历dist目录下的所有文件
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    file_path = Path(root) / file
                    # 在压缩包中的相对路径
                    arcname = file_path.relative_to(dist_dir)
                    zipf.write(file_path, arcname)
                    print(f"  添加文件: {arcname}")
        
        # 显示压缩包信息
        zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ ZIP压缩包创建成功!")
        print(f"📦 压缩包文件: {zip_path}")
        print(f"📏 压缩包大小: {zip_size:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建ZIP压缩包失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 B站答题助手GUI打包工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请先安装必要的依赖")
        sys.exit(1)
    
    print()
    
    # 清理缓存
    clean_python_cache()
    print()
    
    # 清理之前的构建文件
    clean_build_dirs()
    print()
    
    # 构建可执行文件
    if build_executable():
        print()
        # 创建ZIP压缩包
        if create_zip_package():
            print()
            print("🎉 构建和打包完成！")
            print("📁 可执行文件位于 dist/ 目录中")
            print("📦 ZIP压缩包已创建，可直接分发使用")
        else:
            print()
            print("⚠️  构建成功，但ZIP打包失败")
            print("📁 可执行文件位于 dist/ 目录中")
    else:
        print("❌ 构建失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 