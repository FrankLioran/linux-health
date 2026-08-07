#start.sh
#!/bin/bash

cd ~/linux-health || exit

if [ -d "venv" ]; then
    source venv/bin/activate
fi

clear

echo "========================================"
echo "      Linux Health Manager"
echo "========================================"
echo

python3 health.py

status=$?

echo
echo "Programma afgesloten met status: $status"
echo
read -p "Druk op Enter..."