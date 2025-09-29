@echo off
echo VFS Emulator - Stage 3 VFS Testing

echo.
echo 1. Testing minimal VFS:
python main.py --vfs minimal_vfs.xml --script test_vfs_commands.txt

echo.
echo 2. Testing multi-file VFS:
python main.py --vfs multi_file_vfs.xml --debug

echo.
echo 3. Testing deep directory structure:
python main.py --vfs deep_vfs.xml

echo.
echo 4. Testing without VFS:
python main.py --debug

echo.
echo VFS testing completed!
pause