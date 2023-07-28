#!/bin/bash

# 檢查是否有提供容器名稱和目錄名稱
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <container_name> <directory_name>"
    exit 1
fi

# 從腳本參數獲取容器名稱和目錄名稱
CONTAINER_NAME=$1
DIRECTORY_NAME=$2

# 獲取當前日期
TODAY=$(date +%Y%m%d)

# 創建並運行一個臨時的 Ubuntu 容器，並將當前目錄掛載到容器的 /backup 目錄
# 使用 --volumes-from 參數來共享指定容器的 volume
# 使用 tar 指令來打包並壓縮指定目錄的內容
docker run --rm --volumes-from $CONTAINER_NAME -v $(pwd):/backup ubuntu tar cvf /backup/$CONTAINER_NAME$TODAY.tar $DIRECTORY_NAME

echo "Backup completed successfully."
