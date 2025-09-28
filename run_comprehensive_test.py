#!/usr/bin/env python3
"""
Comprehensive test script for Stage 2
Tests all configuration features
"""

import subprocess
import sys
import os

def run_test(description, command, input_text=None):
    """Run a test and report results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"COMMAND: {command}")
    print('='*60)
    
    try:
        if input_text:
            result = subprocess.run(
                command,
                input=input_text,
                capture_output=True,
                text=True,
                shell=True
            )
        else:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )
        
        print("OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "PASS" if success else "FAIL"
        print(f"RESULT: {status}")
        
        return success
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("VFS Emulator - Stage 2 Comprehensive Test")
    print("Testing all configuration features...")
    
    tests = [
        {
            "desc": "1. Help command",
            "cmd": "python main.py --help",
            "input": None
        },
        {
            "desc": "2. Debug mode with commands", 
            "cmd": "python main.py --debug",
            "input": "config\npwd\nexit\n"
        },
        {
            "desc": "3. Startup script execution",
            "cmd": "python main.py --script startup_demo.txt",
            "input": None
        },
        {
            "desc": "4. VFS parameter",
            "cmd": "python main.py --vfs test.xml",
            "input": "config\nexit\n"
        },
        {
            "desc": "5. All parameters combined",
            "cmd": "python main.py --vfs test.xml --script test_script.txt --debug", 
            "input": None
        },
        {
            "desc": "6. Error handling - missing script",
            "cmd": "python main.py --script missing.txt",
            "input": "exit\n"
        }
    ]
    
    passed = 0
    for test in tests:
        if run_test(test["desc"], test["cmd"], test["input"]):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY: {passed}/{len(tests)} tests passed")
    if passed == len(tests):
        print("🎉 All tests passed! Stage 2 implementation is correct.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    print('='*60)

if __name__ == "__main__":
    main()