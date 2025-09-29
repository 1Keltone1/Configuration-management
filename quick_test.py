#!/usr/bin/env python3
"""
Быстрый тест Stage 4 команд
"""

import subprocess
import sys

def test_command(description, commands):
    print(f"\n🔍 {description}")
    print("-" * 50)
    
    cmd = [sys.executable, "main.py", "--vfs", "unix_like_vfs.xml"]
    
    try:
        result = subprocess.run(
            cmd,
            input=commands,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Показываем ключевые строки вывода
        for line in result.stdout.split('\n'):
            if any(keyword in line for keyword in ['$', 'up ', 'user ', 'total ', 'drwx', '-rw-', 'cd:', 'ls:']):
                print(f"  {line}")
                
    except Exception as e:
        print(f"  Error: {e}")

# Запуск тестов
print("🚀 Stage 4 Quick Tests")
print("=" * 50)

test_command("ls -l detailed output", "ls -l /\nls -l /home\nexit")
test_command("cd navigation", "cd /home/user\npwd\ncd ..\npwd\ncd /var/log\npwd\nexit")
test_command("uptime and who", "uptime\nwho\nexit")
test_command("Error handling", "cd /invalid\nls /nonexistent\ncat /missing\nexit")

print("\n✅ Quick tests completed")