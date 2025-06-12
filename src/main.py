import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, qInstallMessageHandler, QtMsgType
from browser import Browser

def message_handler(mode, context, message):
    """自定义消息处理器，过滤掉不需要的输出"""
    # 过滤掉JavaScript相关的输出
    if mode == QtMsgType.QtInfoMsg and 'js:' in message:
        return
    if mode == QtMsgType.QtWarningMsg and ('js:' in message or 'DevTools' in message):
        return
    
    # 只输出错误级别的消息（如果需要）
    if mode == QtMsgType.QtCriticalMsg or mode == QtMsgType.QtFatalMsg:
        print(f"Error: {message}")

def main():
    # 安装自定义消息处理器
    qInstallMessageHandler(message_handler)
    
    # 启用Chrome DevTools
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"
    
    # 设置环境变量来减少日志输出
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-logging --log-level=3"
    
    # 启用高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("手机模拟浏览器")
    
    # 启用开发者工具
    app.setApplicationDisplayName("手机模拟浏览器")
    
    # 创建并显示浏览器窗口
    browser = Browser()
    browser.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()