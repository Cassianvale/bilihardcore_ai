#!/usr/bin/env python3
"""
Local build script
Support building applications in local environment for development and testing
"""

import os
import sys
import shutil
import platform
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True, shell=None):
    """Run command and handle output"""
    if shell is None:
        shell = platform.system() == "Windows"
    
    print(f"[EXEC] Running: {cmd}")
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
        print(f"[ERROR] Command failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        if check:
            sys.exit(1)
        return e

def clean_build():
    """Clean build directories"""
    print("[CLEAN] Cleaning build directories...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  [OK] Removed {dir_name}")
    
    # Clean spec files
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"  [OK] Removed {spec_file}")

def check_dependencies():
    """Check dependencies"""
    print("[CHECK] Checking dependencies...")
    
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
            print(f"  [OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  [MISSING] {package}")
    
    if missing_packages:
        print(f"\n[ERROR] Missing packages: {', '.join(missing_packages)}")
        print("[INFO] Run: pip install -r requirements.txt")
        return False
    
    return True

def generate_spec():
    """Generate PyInstaller spec file"""
    print("[SPEC] Generating PyInstaller spec file...")
    
    # Check if build_spec.py exists
    if not Path('build_spec.py').exists():
        print("[ERROR] build_spec.py not found!")
        return False
    
    # Run generation script
    result = run_command([sys.executable, 'build_spec.py'])
    return result.returncode == 0

def build_app(console=False, onefile=False):
    """Build application"""
    print("[BUILD] Building application...")
    
    # Check spec file
    spec_file = Path('BiliHardcore_AI.spec')
    if not spec_file.exists():
        print("[ERROR] Spec file not found! Generating...")
        if not generate_spec():
            return False
    
    # Build command
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
    
    # Execute build
    result = run_command(cmd)
    return result.returncode == 0

def test_executable():
    """Test executable"""
    print("[TEST] Testing executable...")
    
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
        print(f"[ERROR] Executable not found: {app_path}")
        return False
    
    print(f"[OK] Executable found: {app_path}")
    print(f"[INFO] Size: {app_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # List dist directory contents
    dist_dir = Path('dist/BiliHardcore_AI')
    if dist_dir.exists():
        print("\n[INFO] Distribution contents:")
        for item in sorted(dist_dir.iterdir()):
            if item.is_file():
                size = item.stat().st_size / 1024
                print(f"  [FILE] {item.name} ({size:.1f} KB)")
            else:
                print(f"  [DIR] {item.name}/")
    
    return True

def create_package():
    """Create distribution package"""
    print("[PACKAGE] Creating distribution package...")
    
    system = platform.system()
    version = "dev"  # Can be obtained from git tag
    
    # Try to get git version
    try:
        result = run_command(['git', 'describe', '--tags', '--abbrev=0'], check=False)
        if result.returncode == 0:
            version = result.stdout.strip()
    except:
        pass
    
    # Determine package name and format
    if system == "Windows":
        package_name = f"BiliHardcore_AI-{version}-windows-x64.zip"
        # Create ZIP package
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
        print(f"[OK] Package created: {package_name} ({size:.1f} MB)")
        return True
    else:
        print(f"[ERROR] Failed to create package: {package_name}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Local build script')
    parser.add_argument('--clean', action='store_true', help='Clean build directories')
    parser.add_argument('--console', action='store_true', help='Build console version')
    parser.add_argument('--onefile', action='store_true', help='Build single file version')
    parser.add_argument('--no-test', action='store_true', help='Skip testing')
    parser.add_argument('--no-package', action='store_true', help='Skip packaging')
    
    args = parser.parse_args()
    
    print("BiliHardcore AI Auto Answer Tool - Local Build Script")
    print(f"Platform: {platform.platform()}")
    print(f"Python: {sys.version}")
    print()
    
    # Make sure we're in project root directory
    if not Path('run.py').exists():
        print("[ERROR] Please run this script in project root directory")
        sys.exit(1)
    
    try:
        # Clean
        if args.clean:
            clean_build()
        
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Generate spec file
        if not generate_spec():
            sys.exit(1)
        
        # Build
        if not build_app(console=args.console, onefile=args.onefile):
            sys.exit(1)
        
        # Test
        if not args.no_test:
            if not test_executable():
                sys.exit(1)
        
        # Package
        if not args.no_package:
            if not create_package():
                sys.exit(1)
        
        print("\n[SUCCESS] Build completed!")
        
    except KeyboardInterrupt:
        print("\n[WARNING] Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 