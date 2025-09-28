#!/usr/bin/env python3
"""
Demo script for Stage 1 - REPL
Shows emulator work in interactive mode
"""

def demo_interactive_session():
    """Demonstrates example interactive session"""
    print("=== VFS Emulator Demo ===\n")
    
    # Simulate command work
    commands = [
        "help",
        "pwd",
        "ls",
        "ls -l",
        "cd /home",
        "pwd", 
        "ls",
        "cd ..",
        "pwd",
        "cd invalid/path",
        "invalid_command",
        "cd /",
        "exit"
    ]
    
    current_dir = "/"
    
    for cmd in commands:
        print(f"{current_dir}$ {cmd}")
        
        if cmd == "help":
            print("""
Available commands:
  ls [args]     - List directory contents (stub)
  cd [dir]      - Change directory (stub)  
  pwd           - Print current directory
  exit          - Exit the emulator
  help          - Show this help message
""")
        elif cmd == "pwd":
            print(current_dir)
        elif cmd.startswith("ls"):
            args = cmd[2:].strip()
            print(f"Command: ls, Arguments: {args if args else '[]'}")
            print("file1.txt  file2.txt  directory1/")
        elif cmd.startswith("cd"):
            arg = cmd[2:].strip()
            if not arg:
                current_dir = "/"
                print("Changed to root directory")
            elif arg == "..":
                if current_dir != "/":
                    parts = current_dir.rstrip('/').split('/')
                    if len(parts) > 1:
                        current_dir = '/'.join(parts[:-1]) + '/'
                        if current_dir == "":
                            current_dir = "/"
                print(f"Changed to parent directory: {current_dir}")
            elif arg.startswith("/"):
                current_dir = arg if arg.endswith("/") else arg + "/"
                print(f"Changed to directory: {current_dir}")
            else:
                if current_dir == "/":
                    current_dir = f"/{arg}/"
                else:
                    current_dir = f"{current_dir}{arg}/"
                print(f"Changed to directory: {current_dir}")
        elif cmd == "invalid_command":
            print("Error: Unknown command 'invalid_command'")
        elif cmd == "exit":
            print("Exiting emulator...")
            break
            
        print()

if __name__ == "__main__":
    demo_interactive_session()