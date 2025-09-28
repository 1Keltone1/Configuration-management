#!/usr/bin/env python3
"""
Console version of VFS Emulator for environments without GUI
"""

import sys
import os

class ConsoleVFSEmulator:
    def __init__(self):
        self.current_directory = "/"
        self.running = True
        self.commands = {
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'help': self.cmd_help,
            'exit': self.cmd_exit
        }
        
    def print_prompt(self):
        print(f"{self.current_directory}$ ", end='')
        
    def parse_command(self, command_string):
        """Command parser - splits input into command and arguments by spaces"""
        if not command_string.strip():
            return "", []
            
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        for char in command_string:
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current_part += char
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
                
        if current_part:
            parts.append(current_part)
            
        if len(parts) == 0:
            return "", []
            
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args
        
    def execute_command(self, command_string):
        command, args = self.parse_command(command_string)
        command = command.lower()
        
        if command in self.commands:
            self.commands[command](args)
        elif command:
            print(f"Error: Unknown command '{command}'")
            
    def cmd_ls(self, args):
        """ls command - stub"""
        print(f"Command: ls, Arguments: {args}")
        print("file1.txt  file2.txt  directory1/")
        
    def cmd_cd(self, args):
        """cd command - stub"""
        print(f"Command: cd, Arguments: {args}")
        
        if len(args) == 0:
            self.current_directory = "/"
            print("Changed to root directory")
        elif len(args) == 1:
            if args[0] == "..":
                if self.current_directory != "/":
                    parts = self.current_directory.rstrip('/').split('/')
                    if len(parts) > 1:
                        self.current_directory = '/'.join(parts[:-1]) + '/'
                        if self.current_directory == "":
                            self.current_directory = "/"
                    else:
                        self.current_directory = "/"
                print(f"Changed to parent directory: {self.current_directory}")
            elif args[0] == "/":
                self.current_directory = "/"
                print("Changed to root directory")
            else:
                new_dir = args[0]
                if new_dir.startswith("/"):
                    self.current_directory = new_dir if new_dir.endswith("/") else new_dir + "/"
                else:
                    if self.current_directory == "/":
                        self.current_directory = f"/{new_dir}/"
                    else:
                        self.current_directory = f"{self.current_directory}{new_dir}/"
                print(f"Changed to directory: {self.current_directory}")
        else:
            print("Error: cd: too many arguments")
            
    def cmd_pwd(self, args=None):
        """pwd command - shows current directory"""
        print(self.current_directory)
        
    def cmd_help(self, args=None):
        """help command - shows available commands"""
        help_text = """
Available commands:
  ls [args]     - List directory contents (stub)
  cd [dir]      - Change directory (stub)  
  pwd           - Print current directory
  exit          - Exit the emulator
  help          - Show this help message
"""
        print(help_text)
        
    def cmd_exit(self, args=None):
        """exit command - quits the emulator"""
        print("Exiting VFS Emulator...")
        self.running = False
        
    def run(self):
        print("VFS Emulator v1.0 - Console Version")
        print("Type 'exit' to quit, 'help' for available commands")
        print("-" * 50)
        
        while self.running:
            try:
                self.print_prompt()
                command_string = input().strip()
                self.execute_command(command_string)
                print()  # Empty line for better readability
            except KeyboardInterrupt:
                print("\nUse 'exit' command to quit")
            except EOFError:
                print("\nExiting...")
                break

def main():
    emulator = ConsoleVFSEmulator()
    emulator.run()

if __name__ == "__main__":
    main()