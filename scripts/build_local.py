#!/usr/bin/env python3
"""
本地构建脚本
支持在本地环境中构建应用程序，方便开发和测试
"""

import os
import sys
import shutil
import platform
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True, shell=None):
    """运行命令并处理输出"""
    if shell is None:
        shell = platform.system() == "Windows"
    
    print(f"🚀 Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=check, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        if check:
            sys.exit(1)
        return e

def clean_build():
    """清理构建目录"""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  ✅ Removed {dir_name}")
    
    # 清理spec文件
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"  ✅ Removed {spec_file}")

def check_dependencies():
    """检查依赖项"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'PySide6',
        'pyinstaller',
        'requests',
        'qrcode',
        'loguru',
        'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    return True

def generate_spec():
    """生成PyInstaller spec文件"""
    print("📝 Generating PyInstaller spec file...")
    
    # 检查build_spec.py是否存在
    if not Path('build_spec.py').exists():
        print("❌ build_spec.py not found!")
        return False
    
    # 运行生成脚本
    result = run_command([sys.executable, 'build_spec.py'])
    return result.returncode == 0

def build_app(console=False, onefile=False):
    """构建应用程序"""
    print("🔨 Building application...")
    
    # 检查spec文件
    spec_file = Path('BiliHardcore_AI.spec')
    if not spec_file.exists():
        print("❌ Spec file not found! Generating...")
        if not generate_spec():
            return False
    
    # 构建命令
    cmd = [sys.executable, '-m', 'PyInstaller']
    
    if console:
        cmd.append('--console')
    else:
        cmd.append('--windowed')
    
    if onefile:
        cmd.append('--onefile')
    else:
        cmd.append('--onedir')
    
    cmd.extend([
        '--clean',
        '--noconfirm',
        str(spec_file)
    ])
    
    # 执行构建
    result = run_command(cmd)
    return result.returncode == 0

def test_executable():
    """测试可执行文件"""
    print("🧪 Testing executable...")
    
    system = platform.system()
    app_path = None
    
    if system == "Windows":
        app_path = Path('dist/BiliHardcore_AI/BiliHardcore_AI.exe')
    elif system == "Darwin":
        app_path = Path('dist/BiliHardcore_AI.app')
        if not app_path.exists():
            app_path = Path('dist/BiliHardcore_AI/BiliHardcore_AI')
    else:  # Linux
        app_path = Path('dist/BiliHardcore_AI/BiliHardcore_AI')
    
    if not app_path.exists():
        print(f"❌ Executable not found: {app_path}")
        return False
    
    print(f"✅ Executable found: {app_path}")
    print(f"📏 Size: {app_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # 列出dist目录内容
    dist_dir = Path('dist/BiliHardcore_AI')
    if dist_dir.exists():
        print("\n📁 Distribution contents:")
        for item in sorted(dist_dir.iterdir()):
            if item.is_file():
                size = item.stat().st_size / 1024
                print(f"  📄 {item.name} ({size:.1f} KB)")
            else:
                print(f"  📁 {item.name}/")
    
    return True

def create_package():
    """创建分发包"""
    print("📦 Creating distribution package...")
    
    system = platform.system()
    version = "dev"  # 可以从git tag获取
    
    # 尝试获取git版本
    try:
        result = run_command(['git', 'describe', '--tags', '--abbrev=0'], check=False)
        if result.returncode == 0:
            version = result.stdout.strip()
    except:
        pass
    
    # 确定包名和格式
    if system == "Windows":
        package_name = f"BiliHardcore_AI-{version}-windows-x64.zip"
        # 创建ZIP包
        import zipfile
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            dist_dir = Path('dist/BiliHardcore_AI')
            for file_path in dist_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(dist_dir.parent)
                    zf.write(file_path, arcname)
    elif system == "Darwin":
        package_name = f"BiliHardcore_AI-{version}-macos-{platform.machine().lower()}.zip"
        run_command(['zip', '-r', package_name, 'dist/BiliHardcore_AI'])
    else:  # Linux
        package_name = f"BiliHardcore_AI-{version}-linux-x64.tar.gz"
        run_command(['tar', '-czf', package_name, '-C', 'dist', 'BiliHardcore_AI'])
    
    if Path(package_name).exists():
        size = Path(package_name).stat().st_size / 1024 / 1024
        print(f"✅ Package created: {package_name} ({size:.1f} MB)")
        return True
    else:
        print(f"❌ Failed to create package: {package_name}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='本地构建脚本')
    parser.add_argument('--clean', action='store_true', help='清理构建目录')
    parser.add_argument('--console', action='store_true', help='构建控制台版本')
    parser.add_argument('--onefile', action='store_true', help='构建单文件版本')
    parser.add_argument('--no-test', action='store_true', help='跳过测试')
    parser.add_argument('--no-package', action='store_true', help='跳过打包')
    
    args = parser.parse_args()
    
    print("🎯 B站硬核会员自动答题工具 - 本地构建脚本")
    print(f"💻 Platform: {platform.platform()}")
    print(f"🐍 Python: {sys.version}")
    print()
    
    # 确保在项目根目录
    if not Path('run.py').exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    try:
        # 清理
        if args.clean:
            clean_build()
        
        # 检查依赖
        if not check_dependencies():
            sys.exit(1)
        
        # 生成spec文件
        if not generate_spec():
            sys.exit(1)
        
        # 构建
        if not build_app(console=args.console, onefile=args.onefile):
            sys.exit(1)
        
        # 测试
        if not args.no_test:
            if not test_executable():
                sys.exit(1)
        
        # 打包
        if not args.no_package:
            if not create_package():
                sys.exit(1)
        
        print("\n🎉 构建完成!")
        
    except KeyboardInterrupt:
        print("\n⚠️ 构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 构建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 