#!/usr/bin/env python3
"""
Comprehensive VFS testing script for Stage 3
"""

import subprocess
import sys
import os

def run_vfs_test(test_name, vfs_file, commands):
    """Run a VFS test"""
    print(f"\n{'='*60}")
    print(f"VFS TEST: {test_name}")
    print(f"VFS File: {vfs_file}")
    print('='*60)
    
    cmd = [sys.executable, "main.py", "--vfs", vfs_file]
    
    try:
        result = subprocess.run(
            cmd,
            input=commands,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
        
        success = result.returncode == 0
        print(f"RESULT: {'PASS' if success else 'FAIL'}")
        return success
        
    except subprocess.TimeoutExpired:
        print("TEST TIMEOUT")
        return False
    except Exception as e:
        print(f"TEST ERROR: {e}")
        return False

def main():
    print("VFS Emulator - Stage 3 Comprehensive VFS Testing")
    
    # Test cases
    test_cases = [
        {
            "name": "Minimal VFS",
            "file": "minimal_vfs.xml",
            "commands": """config
vfsinfo
pwd
ls
ls /home
cat /home/user/readme.txt
exit
"""
        },
        {
            "name": "Multi-file VFS", 
            "file": "multi_file_vfs.xml",
            "commands": """vfsinfo
ls /
ls /home/user
cat /home/user/document.txt
cat /bin/ls
cd /tmp
pwd
cat temp.log
exit
"""
        },
        {
            "name": "Deep Directory Structure",
            "file": "deep_vfs.xml", 
            "commands": """vfsinfo
ls /
cd /root/usr/local/bin
pwd
ls
cd ../../..
pwd
cd /home/users/alice
ls
cat documents
cd ../bob
ls
exit
"""
        },
        {
            "name": "Binary Data VFS",
            "file": "binary_vfs.xml",
            "commands": """vfsinfo
ls /data
cat /data/text_file.txt
cat /data/binary_data.bin
exit
"""
        }
    ]
    
    # Create test VFS files
    print("Creating test VFS files...")
    
    passed = 0
    for test in test_cases:
        if os.path.exists(test["file"]):
            if run_vfs_test(test["name"], test["file"], test["commands"]):
                passed += 1
        else:
            print(f"SKIP: VFS file not found: {test['file']}")
    
    # Test error cases
    print(f"\n{'='*60}")
    print("TESTING ERROR CASES")
    print('='*60)
    
    error_tests = [
        ("Non-existent VFS file", "nonexistent.xml"),
        ("Malformed VFS file", "malformed_vfs.xml"),
    ]
    
    for test_name, vfs_file in error_tests:
        cmd = [sys.executable, "main.py", "--vfs", vfs_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✓ {test_name}: Error handled correctly")
            passed += 1
        else:
            print(f"✗ {test_name}: Should have failed")
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY: {passed}/{len(test_cases) + len(error_tests)} tests passed")
    if passed == len(test_cases) + len(error_tests):
        print("🎉 All VFS tests passed! Stage 3 implementation is correct.")
    else:
        print("❌ Some VFS tests failed.")
    print('='*60)

if __name__ == "__main__":
    main()