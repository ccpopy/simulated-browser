from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtCore import QUrl, pyqtSignal

class CustomWebEnginePage(QWebEnginePage):
    """自定义WebEnginePage，用于屏蔽控制台输出"""
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        """重写控制台消息处理，不输出到终端"""
        pass

class BrowserTab(QWidget):
    """浏览器标签页组件"""
    
    # 信号定义
    title_changed = pyqtSignal(str)
    icon_changed = pyqtSignal()
    url_changed = pyqtSignal(QUrl)
    load_started = pyqtSignal()
    load_finished = pyqtSignal(bool)
    load_progress = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        
        # 使用自定义的WebEnginePage来屏蔽控制台输出
        custom_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(custom_page)
        
        layout.addWidget(self.web_view)
        
        # 连接信号
        self.web_view.titleChanged.connect(self.title_changed.emit)
        self.web_view.iconChanged.connect(self.icon_changed.emit)
        self.web_view.urlChanged.connect(self.url_changed.emit)
        self.web_view.loadStarted.connect(self.load_started.emit)
        self.web_view.loadFinished.connect(self.load_finished.emit)
        self.web_view.loadProgress.connect(self.load_progress.emit)
        
        # 加载默认页面
        self.web_view.load(QUrl("https://www.baidu.com"))
    
    def set_user_agent(self, user_agent):
        """设置User-Agent"""
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(user_agent)
        
        # 重新加载当前页面
        self.web_view.reload()
    
    def navigate_to_url(self, url):
        """导航到指定URL"""
        if not url.startswith(('http://', 'https://')):
            # 检查是否是本地地址
            if ':' in url and url.split(':')[-1].isdigit():
                url = 'http://' + url
            else:
                url = 'https://' + url
        self.web_view.load(QUrl(url))
    
    def can_go_back(self):
        """是否可以后退"""
        return self.web_view.history().canGoBack()
    
    def can_go_forward(self):
        """是否可以前进"""
        return self.web_view.history().canGoForward()
    
    def go_back(self):
        """后退"""
        self.web_view.back()
    
    def go_forward(self):
        """前进"""
        self.web_view.forward()
    
    def reload(self):
        """刷新页面"""
        self.web_view.reload()
    
    def stop(self):
        """停止加载"""
        self.web_view.stop()
    
    def get_url(self):
        """获取当前URL"""
        return self.web_view.url()
    
    def get_title(self):
        """获取页面标题"""
        title = self.web_view.title()
        return title if title else "新标签页"
    
    def get_icon(self):
        """获取页面图标"""
        return self.web_view.icon()
    
    def get_web_view(self):
        """获取WebEngineView实例"""
        return self.web_view