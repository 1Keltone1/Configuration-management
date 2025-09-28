#!/usr/bin/env python3
"""
Demo script for Stage 2: Configuration
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and display output"""
    print(f"\n{'='*60}")
    print(f"DEMO: {description}")
    print(f"COMMAND: {cmd}")
    print(f"{'='*60}")
    
    try:
        if isinstance(cmd, list):
            result = subprocess.run(cmd, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def main():
    print("VFS Emulator - Stage 2: Configuration Demo")
    print("This demo shows all new features implemented in Stage 2")
    
    # Test 1: Basic usage with debug
    run_command(
        [sys.executable, "main.py", "--debug"], 
        "Basic emulator with debug output"
    )
    
    # Test 2: With startup script
    run_command(
        [sys.executable, "main.py", "--script", "startup_demo.txt", "--debug"],
        "Emulator with startup script execution"
    )
    
    # Test 3: With both VFS path and script
    run_command(
        [sys.executable, "main.py", "--vfs", "./test_vfs.xml", "--script", "test_script.txt", "--debug"],
        "Emulator with both VFS path and startup script"
    )
    
    # Test 4: Error case - non-existent script
    run_command(
        [sys.executable, "main.py", "--script", "nonexistent.txt", "--debug"],
        "Error handling for non-existent script"
    )
    
    # Test 5: Help message
    run_command(
        [sys.executable, "main.py", "--help"],
        "Command line help display"
    )
    
    print("\n" + "="*60)
    print("STAGE 2 DEMO COMPLETED")
    print("Implemented features:")
    print("✓ Command line argument parsing")
    print("✓ VFS path parameter")
    print("✓ Startup script parameter") 
    print("✓ Debug mode with parameter output")
    print("✓ Script execution with comment support")
    print("✓ Error handling for script execution")
    print("✓ OS testing scripts")
    print("="*60)

if __name__ == "__main__":
    main()