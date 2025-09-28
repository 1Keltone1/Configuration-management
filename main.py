import tkinter as tk
from tkinter import scrolledtext, Entry, Frame

class VFSEmulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VFS Emulator v1.0")
        self.setup_ui()
        self.current_directory = "/"
        
    def setup_ui(self):
        # Main output area
        self.output_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD,
            width=80,
            height=25,
            bg='black',
            fg='white',
            insertbackground='white',
            font=('Courier New', 10)
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_area.config(state=tk.DISABLED)
        
        # Command input area
        input_frame = Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.prompt_label = tk.Label(
            input_frame, 
            text="$", 
            bg='black', 
            fg='green',
            font=('Courier New', 10, 'bold')
        )
        self.prompt_label.pack(side=tk.LEFT)
        
        self.command_entry = Entry(
            input_frame,
            bg='black',
            fg='white',
            insertbackground='white',
            font=('Courier New', 10),
            width=70
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.focus()
        
        # Welcome message
        self.print_output("VFS Emulator v1.0 - Virtual File System Emulator\n")
        self.print_output("Type 'exit' to quit, 'help' for available commands\n")
        self.update_prompt()
        
    def update_prompt(self):
        self.prompt_label.config(text=f"{self.current_directory}$")
        
    def print_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
        
    def parse_command(self, command_string):
        """Command parser - splits input into command and arguments by spaces"""
        if not command_string.strip():
            return "", []
            
        # Split by spaces, considering quotes
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
        
    def execute_command(self, event=None):
        command_string = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        
        # Display entered command
        self.print_output(f"{self.current_directory}$ {command_string}\n")
        
        if not command_string:
            return
            
        command, args = self.parse_command(command_string)
        command = command.lower()
        
        # Command processing
        if command == "exit":
            self.root.quit()
            
        elif command == "ls":
            self.cmd_ls(args)
            
        elif command == "cd":
            self.cmd_cd(args)
            
        elif command == "help":
            self.cmd_help()
            
        elif command == "pwd":
            self.cmd_pwd()
            
        else:
            self.print_output(f"Error: Unknown command '{command}'\n")
            
        self.update_prompt()
        
    def cmd_ls(self, args):
        """ls command - stub"""
        self.print_output(f"Command: ls, Arguments: {args}\n")
        self.print_output("file1.txt  file2.txt  directory1/\n")
        
    def cmd_cd(self, args):
        """cd command - stub"""
        self.print_output(f"Command: cd, Arguments: {args}\n")
        
        if len(args) == 0:
            # cd without arguments - go to home directory
            self.current_directory = "/"
            self.print_output("Changed to root directory\n")
        elif len(args) == 1:
            if args[0] == "..":
                # Go up one level
                if self.current_directory != "/":
                    parts = self.current_directory.rstrip('/').split('/')
                    if len(parts) > 1:
                        self.current_directory = '/'.join(parts[:-1]) + '/'
                        if self.current_directory == "":
                            self.current_directory = "/"
                    else:
                        self.current_directory = "/"
                self.print_output(f"Changed to parent directory: {self.current_directory}\n")
            elif args[0] == "/":
                # Go to root directory
                self.current_directory = "/"
                self.print_output("Changed to root directory\n")
            else:
                # Try to go to specified directory
                new_dir = args[0]
                if new_dir.startswith("/"):
                    self.current_directory = new_dir if new_dir.endswith("/") else new_dir + "/"
                else:
                    if self.current_directory == "/":
                        self.current_directory = f"/{new_dir}/"
                    else:
                        self.current_directory = f"{self.current_directory}{new_dir}/"
                self.print_output(f"Changed to directory: {self.current_directory}\n")
        else:
            self.print_output("Error: cd: too many arguments\n")
            
    def cmd_help(self):
        """help command - shows available commands"""
        help_text = """
Available commands:
  ls [args]     - List directory contents (stub)
  cd [dir]      - Change directory (stub)  
  pwd           - Print current directory
  exit          - Exit the emulator
  help          - Show this help message

"""
        self.print_output(help_text)
        
    def cmd_pwd(self):
        """pwd command - shows current directory"""
        self.print_output(f"{self.current_directory}\n")
        
    def run(self):
        self.root.mainloop()

def main():
    emulator = VFSEmulator()
    emulator.run()

if __name__ == "__main__":
    main()