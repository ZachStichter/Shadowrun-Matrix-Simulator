@echo off
start /min "" wsl -d Ubuntu bash -c "nohup ollama serve > /dev/null 2>&1; sleep 5; exit"
exit