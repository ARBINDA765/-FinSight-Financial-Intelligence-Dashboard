#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all files and configurations are ready for deployment
"""

import os
import sys
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("=" * 60)
    print("  FinSight - Setup Verification")
    print("=" * 60)
    print(f"{Colors.END}\n")

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_file_content(filepath, search_string, description):
    """Check if a file contains specific content"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            found = search_string in content
            status = f"{Colors.GREEN}✓{Colors.END}" if found else f"{Colors.RED}✗{Colors.END}"
            print(f"{status} {description}")
            return found
    except:
        print(f"{Colors.RED}✗{Colors.END} {description} (file not readable)")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print(f"\n{Colors.BOLD}Checking Python Packages:{Colors.END}")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'requests',
        'feedparser'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Colors.GREEN}✓{Colors.END} {package}")
        except ImportError:
            print(f"{Colors.RED}✗{Colors.END} {package} (not installed)")
            all_installed = False
    
    return all_installed

def main():
    print_header()
    
    checks_passed = 0
    checks_failed = 0
    
    # Check core files
    print(f"{Colors.BOLD}Checking Core Files:{Colors.END}")
    files_to_check = [
        ('app.py', 'Main dashboard application'),
        ('news_fetch.py', 'News fetching script'),
        ('requirements.txt', 'Python dependencies'),
    ]
    
    for filepath, description in files_to_check:
        if check_file(filepath, description):
            checks_passed += 1
        else:
            checks_failed += 1
    
    # Check GitHub Actions workflow
    print(f"\n{Colors.BOLD}Checking GitHub Actions Configuration:{Colors.END}")
    workflow_dir = '.github/workflows'
    workflow_file = os.path.join(workflow_dir, 'update_news.yml')
    
    if check_directory(workflow_dir, 'Workflow directory'):
        checks_passed += 1
    else:
        checks_failed += 1
    
    if check_file(workflow_file, 'Workflow file'):
        checks_passed += 1
        # Check workflow content
        if check_file_content(workflow_file, 'python news_fetch.py', 
                              'Workflow runs news_fetch.py'):
            checks_passed += 1
        else:
            checks_failed += 1
    else:
        checks_failed += 2
    
    # Check Streamlit configuration
    print(f"\n{Colors.BOLD}Checking Streamlit Configuration:{Colors.END}")
    streamlit_dir = '.streamlit'
    config_file = os.path.join(streamlit_dir, 'config.toml')
    
    if check_directory(streamlit_dir, 'Streamlit config directory'):
        checks_passed += 1
    else:
        checks_failed += 1
    
    if check_file(config_file, 'Streamlit config file'):
        checks_passed += 1
    else:
        checks_failed += 1
    
    # Check Python packages
    if check_python_packages():
        checks_passed += 1
    else:
        checks_failed += 1
        print(f"\n{Colors.YELLOW}⚠ Install missing packages with:{Colors.END}")
        print(f"  pip install -r requirements.txt\n")
    
    # Check if CSV exists (optional)
    print(f"\n{Colors.BOLD}Checking Data Files (Optional):{Colors.END}")
    if check_file('finance_news.csv', 'News data CSV'):
        print(f"  {Colors.YELLOW}Note: CSV will be created by news_fetch.py{Colors.END}")
    else:
        print(f"  {Colors.YELLOW}⚠ CSV not found - run 'python news_fetch.py' to create it{Colors.END}")
    
    # Final summary
    print(f"\n{Colors.BOLD}=" * 60)
    print(f"Summary{Colors.END}")
    print("=" * 60)
    
    total_checks = checks_passed + checks_failed
    print(f"Total checks: {total_checks}")
    print(f"{Colors.GREEN}Passed: {checks_passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {checks_failed}{Colors.END}")
    
    print("\n" + "=" * 60)
    
    if checks_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL CHECKS PASSED!{Colors.END}")
        print(f"{Colors.GREEN}Your setup is ready for deployment.{Colors.END}\n")
        print("Next steps:")
        print("1. Test locally: python news_fetch.py && streamlit run app.py")
        print("2. Push to GitHub: git add . && git commit -m 'Setup deployment' && git push")
        print("3. Follow DEPLOYMENT_GUIDE.md for Streamlit Cloud deployment")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SETUP INCOMPLETE{Colors.END}")
        print(f"{Colors.RED}Please fix the failed checks above.{Colors.END}\n")
        print("Common fixes:")
        print("- Missing files: Copy from deployment files")
        print("- Missing packages: pip install -r requirements.txt")
        print("- Missing directories: Create .github/workflows/ and .streamlit/")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
