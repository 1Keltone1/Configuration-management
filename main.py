#!/usr/bin/env python3
"""
VFS Emulator - Stage 2: Configuration
Enhanced with command line parameters and startup scripts
"""

import sys
import os
import argparse

class VFSConfig:
    """Configuration class for VFS Emulator"""
    
    def __init__(self):
        self.vfs_path = None
        self.startup_script = None
        self.debug_mode = False
        
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='VFS Emulator - Virtual File System Emulator',
            epilog='Example: python main.py --vfs ./vfs.xml --script startup.txt --debug'
        )
        
        parser.add_argument(
            '--vfs', 
            dest='vfs_path',
            metavar='PATH',
            help='Path to VFS physical location (XML file)'
        )
        
        parser.add_argument(
            '--script', 
            dest='startup_script',
            metavar='SCRIPT',
            help='Path to startup script'
        )
        
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug output'
        )
        
        args = parser.parse_args()
        
        self.vfs_path = args.vfs_path
        self.startup_script = args.startup_script
        self.debug_mode = args.debug
        
        # Debug output of all parameters
        if self.debug_mode:
            self._print_debug_info()
        
        return self
    
    def _print_debug_info(self):
        """Print debug information about configuration"""
        print("=== VFS Emulator Configuration ===")
        print(f"VFS Path: {self.vfs_path}")
        print(f"Startup Script: {self.startup_script}")
        print(f"Debug Mode: {self.debug_mode}")
        print("==================================")

class ScriptRunner:
    """Class for executing startup scripts"""
    
    def __init__(self, config):
        self.config = config
        
    def execute_script(self, script_path):
        """Execute startup script with comment support"""
        if not os.path.exists(script_path):
            print(f"Error: Script file not found: {script_path}")
            return False
            
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            print(f"\n=== Executing startup script: {script_path} ===\n")
            
            line_number = 0
            for line in lines:
                line_number += 1
                original_line = line.rstrip()
                line = line.strip()
                
                # Skip empty lines and comments
                if not line:
                    continue
                if line.startswith('#'):
                    if self.config.debug_mode:
                        print(f"[DEBUG] Line {line_number}: Comment - {line}")
                    continue
                
                # Display the command being executed (simulate user input)
                print(f"$ {original_line}")
                
                # Execute the command
                success = self._execute_command(line)
                if not success:
                    print(f"Error in script at line {line_number}: {line}")
                    return False
                    
                print()  # Empty line for readability
                
            print(f"=== Script execution completed: {script_path} ===\n")
            return True
            
        except Exception as e:
            print(f"Error reading script {script_path}: {str(e)}")
            return False
    
    def _execute_command(self, command_line):
        """Execute a single command (stub implementation)"""
        # This is a simplified version - in real implementation
        # this would call the actual command processor
        parts = command_line.split()
        if not parts:
            return True
            
        command = parts[0].lower()
        args = parts[1:]
        
        if command == "pwd":
            print("/home/user")
        elif command == "ls":
            if args:
                print(f"Command: ls, Arguments: {args}")
            print("file1.txt  file2.txt  documents/  downloads/")
        elif command == "cd":
            if args:
                print(f"Changing directory to: {args[0]}")
            else:
                print("Changing to home directory")
        elif command == "config":
            print("Current configuration:")
            print(f"  VFS Path: {self.config.vfs_path or 'Not specified'}")
            print(f"  Startup Script: {self.config.startup_script or 'Not specified'}")
        elif command == "echo":
            print(' '.join(args))
        else:
            print(f"Command executed: {command_line}")
            
        return True

class VFSEmulator:
    """Main VFS Emulator class"""
    
    def __init__(self, config):
        self.config = config
        self.script_runner = ScriptRunner(config)
        self.current_directory = "/"
        
    def run(self):
        """Main execution loop"""
        print("VFS Emulator v2.0 - Configuration Stage")
        print("=" * 50)
        
        # Execute startup script if specified
        if self.config.startup_script:
            if not self.script_runner.execute_script(self.config.startup_script):
                print("Failed to execute startup script. Starting interactive mode...")
        
        # Start interactive mode
        self._interactive_mode()
    
    def _interactive_mode(self):
        """Interactive command loop"""
        print("Interactive mode. Type 'help' for commands, 'exit' to quit.")
        print("-" * 50)
        
        while True:
            try:
                command = input(f"{self.current_directory}$ ").strip()
                
                if not command:
                    continue
                    
                if command.lower() == 'exit':
                    print("Exiting VFS Emulator...")
                    break
                elif command.lower() == 'help':
                    self._show_help()
                else:
                    self._execute_interactive_command(command)
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nExiting...")
                break
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
Available commands:
  pwd          - Print current directory
  ls [path]    - List directory contents
  cd [dir]     - Change directory
  config       - Show current configuration
  echo [text]  - Display text
  help         - Show this help message
  exit         - Exit the emulator
"""
        print(help_text)
    
    def _execute_interactive_command(self, command_line):
        """Execute a command in interactive mode"""
        parts = command_line.split()
        command = parts[0].lower()
        args = parts[1:]
        
        if command == "pwd":
            print(self.current_directory)
        elif command == "ls":
            print(f"Command: ls, Arguments: {args}")
            print("file1.txt  file2.txt  documents/  downloads/")
        elif command == "cd":
            if not args:
                self.current_directory = "/"
                print("Changed to root directory")
            elif args[0] == "..":
                # Simple parent directory handling
                if self.current_directory != "/":
                    parts = self.current_directory.rstrip('/').split('/')
                    if len(parts) > 1:
                        self.current_directory = '/'.join(parts[:-1]) + '/'
                        if self.current_directory == "":
                            self.current_directory = "/"
                print(f"Changed to: {self.current_directory}")
            else:
                new_dir = args[0]
                if new_dir.startswith("/"):
                    self.current_directory = new_dir
                else:
                    if self.current_directory == "/":
                        self.current_directory = f"/{new_dir}"
                    else:
                        self.current_directory = f"{self.current_directory}/{new_dir}"
                if not self.current_directory.endswith("/"):
                    self.current_directory += "/"
                print(f"Changed to: {self.current_directory}")
        elif command == "config":
            print("Current configuration:")
            print(f"  VFS Path: {self.config.vfs_path or 'Not specified'}")
            print(f"  Startup Script: {self.config.startup_script or 'Not specified'}")
            print(f"  Debug Mode: {self.config.debug_mode}")
        elif command == "echo":
            print(' '.join(args))
        else:
            print(f"Unknown command: {command}")

def main():
    """Main entry point"""
    try:
        # Parse command line arguments
        config = VFSConfig().parse_arguments()
        
        # Create and run emulator
        emulator = VFSEmulator(config)
        emulator.run()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()