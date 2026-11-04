#!/usr/bin/env sh
# macOS / Linux 启动入口（Windows 用 启动讲义.cmd）
set -e
cd "$(dirname "$0")"
exec python3 -X utf8 launch.py "$@"
