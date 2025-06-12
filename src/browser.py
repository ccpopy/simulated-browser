from PyQt5.QtWidgets import (QMainWindow, QToolBar, QLineEdit, QTabWidget, QComboBox, QAction, QMenu, QMenuBar, QMessageBox)
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from browser_tab import BrowserTab
from user_agents import USER_AGENTS
import os

class Browser(QMainWindow):
    """主浏览器窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义浏览器")
        self.setGeometry(100, 100, 1200, 800)
        
        self.init_ui()
        self.create_first_tab()
        
    def init_ui(self):
        """初始化UI"""
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建标签页控件
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        
        self.setCentralWidget(self.tabs)
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        new_tab_action = QAction("新建标签页", self)
        new_tab_action.setShortcut(QKeySequence.New)
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("导航")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 设置图标大小
        toolbar.setIconSize(QSize(24, 24))
        
        # 后退按钮
        self.back_action = QAction(self)
        self.back_action.setIcon(self.load_icon("back.svg"))
        self.back_action.setToolTip("后退")
        self.back_action.triggered.connect(self.navigate_back)
        toolbar.addAction(self.back_action)
        
        # 前进按钮
        self.forward_action = QAction(self)
        self.forward_action.setIcon(self.load_icon("forward.svg"))
        self.forward_action.setToolTip("前进")
        self.forward_action.triggered.connect(self.navigate_forward)
        toolbar.addAction(self.forward_action)
        
        # 刷新/停止按钮
        self.reload_action = QAction(self)
        self.reload_action.setIcon(self.load_icon("refresh.svg"))
        self.reload_action.setToolTip("刷新")
        self.reload_action.triggered.connect(self.reload_page)
        toolbar.addAction(self.reload_action)
        
        self.stop_action = QAction(self)
        self.stop_action.setIcon(self.load_icon("stop.svg"))
        self.stop_action.setToolTip("停止")
        self.stop_action.triggered.connect(self.stop_loading)
        self.stop_action.setVisible(False)
        toolbar.addAction(self.stop_action)
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        
        # User-Agent选择器
        self.user_agent_combo = QComboBox()
        self.user_agent_combo.setMinimumWidth(200)
        self.user_agent_combo.addItems(list(USER_AGENTS.keys()))
        self.user_agent_combo.currentTextChanged.connect(self.change_user_agent)
        self.user_agent_combo.setToolTip("切换设备User-Agent")
        toolbar.addWidget(self.user_agent_combo)
        
        # 新建标签页按钮
        new_tab_action = QAction(self)
        new_tab_action.setIcon(self.load_icon("add.svg"))
        new_tab_action.setToolTip("新建标签页")
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_tab_action)
        
    def load_icon(self, filename):
        """加载图标"""
        icon_path = os.path.join("icons", filename)
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        else:
            # 如果图标不存在，创建一个默认图标
            return self.style().standardIcon(self.get_standard_icon(filename))
    
    def get_standard_icon(self, filename):
        """获取标准图标"""
        icon_map = {
            "back.svg": self.style().SP_ArrowBack,
            "forward.svg": self.style().SP_ArrowForward,
            "refresh.svg": self.style().SP_BrowserReload,
            "stop.svg": self.style().SP_BrowserStop,
            "add.svg": self.style().SP_FileDialogNewFolder
        }
        return icon_map.get(filename, self.style().SP_ComputerIcon)
    
    def create_first_tab(self):
        """创建第一个标签页"""
        self.add_new_tab()
        
    def add_new_tab(self):
        """添加新标签页"""
        browser_tab = BrowserTab()
        
        # 连接信号
        browser_tab.title_changed.connect(lambda title: self.update_tab_title(browser_tab, title))
        browser_tab.url_changed.connect(self.update_url_bar)
        browser_tab.load_started.connect(self.on_load_started)
        browser_tab.load_finished.connect(self.on_load_finished)
        
        index = self.tabs.addTab(browser_tab, "新标签页")
        self.tabs.setCurrentIndex(index)
        
        # 设置当前的User-Agent
        current_ua = USER_AGENTS[self.user_agent_combo.currentText()]
        if current_ua:
            browser_tab.set_user_agent(current_ua)
        
        return browser_tab
    
    def close_tab(self, index):
        """关闭标签页"""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # 如果只剩一个标签页，关闭整个窗口
            self.close()
    
    def current_tab_changed(self, index):
        """当前标签页改变时的处理"""
        if index >= 0:
            current_tab = self.tabs.widget(index)
            if current_tab:
                # 更新URL栏
                self.url_bar.setText(current_tab.get_url().toString())
                # 更新前进后退按钮状态
                self.update_navigation_buttons()
    
    def update_tab_title(self, tab, title):
        """更新标签页标题"""
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, title[:30] + "..." if len(title) > 30 else title)
    
    def update_url_bar(self, url):
        """更新地址栏"""
        if self.current_browser() and url == self.current_browser().get_url():
            self.url_bar.setText(url.toString())
            self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        """更新导航按钮状态"""
        browser = self.current_browser()
        if browser:
            self.back_action.setEnabled(browser.can_go_back())
            self.forward_action.setEnabled(browser.can_go_forward())
    
    def on_load_started(self):
        """页面开始加载"""
        self.reload_action.setVisible(False)
        self.stop_action.setVisible(True)
    
    def on_load_finished(self, success):
        """页面加载完成"""
        self.reload_action.setVisible(True)
        self.stop_action.setVisible(False)
    
    def current_browser(self):
        """获取当前浏览器标签页"""
        return self.tabs.currentWidget()
    
    def navigate_to_url(self):
        """导航到URL"""
        url = self.url_bar.text()
        if url:
            browser = self.current_browser()
            if browser:
                browser.navigate_to_url(url)
    
    def navigate_back(self):
        """后退"""
        browser = self.current_browser()
        if browser:
            browser.go_back()
    
    def navigate_forward(self):
        """前进"""
        browser = self.current_browser()
        if browser:
            browser.go_forward()
    
    def reload_page(self):
        """刷新页面"""
        browser = self.current_browser()
        if browser:
            browser.reload()
    
    def stop_loading(self):
        """停止加载"""
        browser = self.current_browser()
        if browser:
            browser.stop()
    
    def change_user_agent(self, ua_name):
        """更改User-Agent"""
        user_agent = USER_AGENTS.get(ua_name, "")
        browser = self.current_browser()
        if browser:
            browser.set_user_agent(user_agent)
    
    def show_dev_tools(self):
        """显示开发者工具"""
        browser = self.current_browser()
        if browser:
            # 获取当前页面的WebEngineView
            web_view = browser.get_web_view()
            page = web_view.page()
            
            # 切换开发者工具的显示状态
            if hasattr(page, 'devToolsPage') and page.devToolsPage():
                # 如果开发者工具已打开，关闭它
                page.setDevToolsPage(None)
            else:
                # 创建新的开发者工具窗口
                dev_view = QWebEngineView()
                dev_view.setWindowTitle("开发者工具")
                dev_view.resize(800, 600)
                page.setDevToolsPage(dev_view.page())
                dev_view.show()
        
    def closeEvent(self, event):
        """关闭事件处理"""
        reply = QMessageBox.question(self, '确认退出', '确定要退出浏览器吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()