#!/bin/bash

echo "=== VFS Emulator - Stage 4 UNIX Commands Testing ==="

echo -e "\n1. Testing enhanced ls command:"
python main.py --vfs unix_like_vfs.xml << EOF
ls -l /
ls -l /home
ls /etc
exit
EOF

echo -e "\n2. Testing cd command logic:"
python main.py --vfs unix_like_vfs.xml << EOF
cd /home/user
pwd
cd ../..
pwd
cd /var/log
pwd
cd /
pwd
exit
EOF

echo -e "\n3. Testing new commands - uptime and who:"
python main.py --vfs unix_like_vfs.xml << EOF
uptime
who
config
exit
EOF

echo -e "\n4. Testing comprehensive script:"
python main.py --vfs unix_like_vfs.xml --script test_unix_commands.txt

echo -e "\n5. Testing error handling:"
python main.py --vfs unix_like_vfs.xml << EOF
cd /nonexistent
ls -l /invalid
cat /missing_file
uptime
who  # Should still work after errors
exit
EOF

echo -e "\n=== Stage 4 testing completed ==="