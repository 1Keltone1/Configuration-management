#!/bin/bash

echo "=== VFS Emulator - Stage 3 VFS Testing ==="

echo -e "\n1. Testing minimal VFS:"
python main.py --vfs minimal_vfs.xml --script test_vfs_commands.txt

echo -e "\n2. Testing multi-file VFS:"
python main.py --vfs multi_file_vfs.xml --debug << EOF
vfsinfo
ls /
ls /home/user
cat /home/user/document.txt
exit
EOF

echo -e "\n3. Testing deep directory structure:"
python main.py --vfs deep_vfs.xml << EOF
vfsinfo
ls /root
ls /root/usr/local/bin
cat /root/system.info
exit
EOF

echo -e "\n4. Testing binary data VFS:"
python main.py --vfs binary_vfs.xml --debug << EOF
ls /data
cat /data/text_file.txt
cat /data/binary_data.bin
exit
EOF

echo -e "\n5. Testing error handling:"
python main.py --vfs invalid_file.xml 2>&1 | head -10
python main.py --vfs malformed_vfs.xml 2>&1 | head -10

echo -e "\n6. Testing without VFS (fallback):"
python main.py --debug << EOF
config
vfsinfo
pwd
ls
exit
EOF

echo -e "\n=== VFS testing completed ==="