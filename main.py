#!/usr/bin/env python3
"""
VFS Emulator - Stage 3: Virtual File System
Enhanced with XML-based VFS loading and in-memory operations
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import base64
from pathlib import Path

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

class VFSNode:
    """Node in the Virtual File System"""
    
    def __init__(self, name, node_type, content=None):
        self.name = name
        self.type = node_type  # 'file' or 'directory'
        self.content = content  # For files: text content or base64 data
        self.children = {} if node_type == 'directory' else None
        self.parent = None
    
    def add_child(self, node):
        """Add a child node to directory"""
        if self.type == 'directory':
            node.parent = self
            self.children[node.name] = node
        else:
            raise ValueError("Can only add children to directories")
    
    def get_path(self):
        """Get full path of this node"""
        path_parts = []
        current = self
        while current:
            path_parts.append(current.name)
            current = current.parent
        return '/' + '/'.join(reversed(path_parts[1:]))  # Skip root node name

class VirtualFileSystem:
    """Virtual File System implementation"""
    
    def __init__(self, config):
        self.config = config
        self.root = VFSNode('', 'directory')
        self.current_directory = self.root
        self.loaded = False
    
    def load_from_xml(self, xml_path):
        """Load VFS from XML file"""
        try:
            if not os.path.exists(xml_path):
                raise FileNotFoundError(f"VFS file not found: {xml_path}")
            
            tree = ET.parse(xml_path)
            root_element = tree.getroot()
            
            if root_element.tag != 'vfs':
                raise ValueError("Invalid VFS format: root element must be 'vfs'")
            
            self._parse_directory(self.root, root_element)
            self.loaded = True
            
            if self.config.debug_mode:
                print(f"[DEBUG] VFS loaded successfully from {xml_path}")
                print(f"[DEBUG] Root directory contains {len(self.root.children)} items")
            
            return True
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
        except Exception as e:
            raise ValueError(f"Error loading VFS: {e}")
    
    def _parse_directory(self, parent_node, xml_element):
        """Parse directory structure from XML"""
        for child in xml_element:
            if child.tag == 'directory':
                dir_name = child.get('name')
                if not dir_name:
                    raise ValueError("Directory missing 'name' attribute")
                
                dir_node = VFSNode(dir_name, 'directory')
                parent_node.add_child(dir_node)
                self._parse_directory(dir_node, child)
                
            elif child.tag == 'file':
                file_name = child.get('name')
                if not file_name:
                    raise ValueError("File missing 'name' attribute")
                
                # Handle file content
                content = child.text.strip() if child.text else ""
                encoding = child.get('encoding', 'text')
                
                if encoding == 'base64':
                    try:
                        # Store base64 content as-is for binary files
                        content = content
                    except Exception as e:
                        raise ValueError(f"Invalid base64 content in file {file_name}: {e}")
                
                file_node = VFSNode(file_name, 'file', content)
                parent_node.add_child(file_node)
    
    def resolve_path(self, path):
        """Resolve a path to a VFS node"""
        if not path or path == '/':
            return self.root
        
        # Handle absolute paths
        if path.startswith('/'):
            current = self.root
            path_parts = path[1:].split('/')
        else:
            # Handle relative paths
            current = self.current_directory
            path_parts = path.split('/')
        
        for part in path_parts:
            if not part or part == '.':
                continue
            elif part == '..':
                if current.parent:
                    current = current.parent
            else:
                if current.type != 'directory' or part not in current.children:
                    return None
                current = current.children[part]
        
        return current
    
    def list_directory(self, path=None):
        """List contents of a directory"""
        target_dir = self.resolve_path(path) if path else self.current_directory
        if not target_dir:
            return None, f"Directory not found: {path}"
        if target_dir.type != 'directory':
            return None, f"Not a directory: {path}"
        
        items = []
        for name, node in target_dir.children.items():
            if node.type == 'directory':
                items.append(f"{name}/")
            else:
                items.append(name)
        
        return sorted(items), None
    
    def change_directory(self, path):
        """Change current directory"""
        target_dir = self.resolve_path(path)
        if not target_dir:
            return f"Directory not found: {path}"
        if target_dir.type != 'directory':
            return f"Not a directory: {path}"
        
        self.current_directory = target_dir
        return None
    
    def get_current_path(self):
        """Get current directory path"""
        return self.current_directory.get_path()
    
    def read_file(self, path):
        """Read file content"""
        file_node = self.resolve_path(path)
        if not file_node:
            return None, f"File not found: {path}"
        if file_node.type != 'file':
            return None, f"Not a file: {path}"
        
        return file_node.content, None

class ScriptRunner:
    """Class for executing startup scripts"""
    
    def __init__(self, emulator):
        self.emulator = emulator
        self.config = emulator.config
    
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
                
                # Display the command being executed
                print(f"$ {original_line}")
                
                # Execute the command
                success = self.emulator.execute_command(line)
                if not success:
                    print(f"Error in script at line {line_number}: {line}")
                    return False
                    
                print()  # Empty line for readability
                
            print(f"=== Script execution completed: {script_path} ===\n")
            return True
            
        except Exception as e:
            print(f"Error reading script {script_path}: {str(e)}")
            return False

class VFSEmulator:
    """Main VFS Emulator class"""
    
    def __init__(self, config):
        self.config = config
        self.vfs = VirtualFileSystem(config)
        self.script_runner = ScriptRunner(self)
        
        # Load VFS if specified
        if config.vfs_path:
            try:
                self.vfs.load_from_xml(config.vfs_path)
                print(f"VFS loaded successfully from: {config.vfs_path}")
            except Exception as e:
                print(f"Error loading VFS: {e}")
                sys.exit(1)
    
    def run(self):
        """Main execution loop"""
        print("VFS Emulator v3.0 - Virtual File System")
        print("=" * 50)
        
        if self.vfs.loaded:
            print(f"VFS: {self.config.vfs_path}")
        else:
            print("VFS: Not loaded (using default empty filesystem)")
        
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
                command = input(f"{self.vfs.get_current_path()}$ ").strip()
                
                if not command:
                    continue
                    
                if command.lower() == 'exit':
                    print("Exiting VFS Emulator...")
                    break
                elif command.lower() == 'help':
                    self._show_help()
                else:
                    self.execute_command(command)
                    
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
  cat [file]   - Display file content
  config       - Show current configuration
  vfsinfo      - Show VFS information
  echo [text]  - Display text
  help         - Show this help message
  exit         - Exit the emulator
"""
        print(help_text)
    
    def execute_command(self, command_line):
        """Execute a command"""
        parts = command_line.split()
        if not parts:
            return True
            
        command = parts[0].lower()
        args = parts[1:]
        
        try:
            if command == "pwd":
                print(self.vfs.get_current_path())
                
            elif command == "ls":
                path = args[0] if args else None
                items, error = self.vfs.list_directory(path)
                if error:
                    print(f"ls: {error}")
                else:
                    print('  '.join(items))
                    
            elif command == "cd":
                path = args[0] if args else "/"
                error = self.vfs.change_directory(path)
                if error:
                    print(f"cd: {error}")
                    
            elif command == "cat":
                if not args:
                    print("cat: missing file operand")
                else:
                    content, error = self.vfs.read_file(args[0])
                    if error:
                        print(f"cat: {error}")
                    else:
                        print(content)
                        
            elif command == "config":
                print("Current configuration:")
                print(f"  VFS Path: {self.config.vfs_path or 'Not specified'}")
                print(f"  Startup Script: {self.config.startup_script or 'Not specified'}")
                print(f"  Debug Mode: {self.config.debug_mode}")
                print(f"  VFS Loaded: {self.vfs.loaded}")
                
            elif command == "vfsinfo":
                if self.vfs.loaded:
                    print("VFS Information:")
                    print(f"  Source: {self.config.vfs_path}")
                    # Count files and directories
                    file_count, dir_count = self._count_vfs_items(self.vfs.root)
                    print(f"  Directories: {dir_count}")
                    print(f"  Files: {file_count}")
                else:
                    print("VFS not loaded")
                    
            elif command == "echo":
                print(' '.join(args))
                
            else:
                print(f"Unknown command: {command}")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error executing command: {e}")
            return False
    
    def _count_vfs_items(self, node):
        """Count files and directories in VFS"""
        if node.type == 'file':
            return 1, 0
        
        file_count = 0
        dir_count = 1  # Count this directory
        
        for child in node.children.values():
            if child.type == 'file':
                file_count += 1
            else:
                child_files, child_dirs = self._count_vfs_items(child)
                file_count += child_files
                dir_count += child_dirs
        
        return file_count, dir_count

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