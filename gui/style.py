STYLE_SHEET = """
/* 全局样式设置 */
QWidget {
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", Arial, sans-serif;
    font-size: 10pt;
    color: #2c3e50;
}

/* 主窗口背景 */
QMainWindow {
    background-color: #f0f2f5;
}

/* 分组框样式 */
QGroupBox {
    font-size: 12pt;
    font-weight: 600;
    border: 2px solid #e1e8ed;
    border-radius: 10px;
    margin-top: 15px;
    padding: 10px;
    padding-top: 5px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    left: 20px;
    color: #2c3e50;
    background-color: #ffffff;
    font-weight: 600;
    min-width: 120px;
    border-radius: 4px;
}

/* 标签样式 */
QLabel {
    font-size: 10pt;
    padding: 3px;
    color: #34495e;
}

/* 输入框样式 */
QLineEdit, QTextEdit {
    border: 2px solid #dde4e9;
    border-radius: 8px;
    padding: 10px;
    background-color: #ffffff;
    font-size: 10pt;
    selection-background-color: #3498db;
    selection-color: #ffffff;
}

QLineEdit:hover, QTextEdit:hover {
    border-color: #b8c5d1;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #3498db;
    outline: none;
}

QLineEdit:disabled, QTextEdit:disabled {
    background-color: #f5f7fa;
    color: #95a5a6;
    border-color: #e1e8ed;
}

/* 下拉框样式 */
QComboBox {
    border: 2px solid #dde4e9;
    border-radius: 6px;
    padding: 8px 12px;
    padding-right: 30px;
    background-color: #ffffff;
    font-size: 10pt;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #b8c5d1;
}

QComboBox:focus {
    border-color: #3498db;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-style: solid;
    border-width: 5px;
    border-top-color: #7f8c8d;
    margin-top: 3px;
}

QComboBox QAbstractItemView {
    border: 1px solid #dde4e9;
    border-radius: 6px;
    background-color: #ffffff;
    selection-background-color: #3498db;
    selection-color: #ffffff;
    padding: 5px;
}

/* 按钮样式 - 使用Qt渐变 */
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #3498db, stop: 1 #2980b9);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 10pt;
    font-weight: 500;
    min-height: 20px;
    text-align: center;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #5dade2, stop: 1 #3498db);
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #2471a3, stop: 1 #1f618d);
    padding-top: 11px;
    padding-bottom: 9px;
}

QPushButton:disabled {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #bdc3c7, stop: 1 #95a5a6);
    color: #ecf0f1;
}

/* 标签页样式 */
QTabWidget::pane {
    border: 2px solid #e1e8ed;
    border-radius: 0 8px 8px 8px;
    background-color: #ffffff;
    padding: 15px;
}

QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #f8f9fa, stop: 1 #e9ecef);
    border: 2px solid #e1e8ed;
    border-bottom: none;
    padding: 10px 20px;
    margin-right: 3px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #7f8c8d;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #2c3e50;
    border-bottom: 2px solid #ffffff;
    margin-bottom: -2px;
}

QTabBar::tab:!selected:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #ffffff, stop: 1 #f1f3f5);
    color: #34495e;
}

/* 日志文本区域特殊样式 */
QTextEdit#log_text {
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 9pt;
    background-color: #2c3e50;
    color: #ecf0f1;
    border: 2px solid #34495e;
    border-radius: 6px;
    padding: 10px;
    line-height: 1.4;
}

/* 滚动条样式 */
QScrollBar:vertical {
    background-color: #f0f3f7;
    width: 14px;
    border-radius: 7px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 #bdc3c7, stop: 1 #95a5a6);
    border-radius: 6px;
    min-height: 30px;
    margin: 1px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 #95a5a6, stop: 1 #7f8c8d);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #f0f3f7;
    height: 14px;
    border-radius: 7px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #bdc3c7, stop: 1 #95a5a6);
    border-radius: 6px;
    min-width: 30px;
    margin: 1px;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #95a5a6, stop: 1 #7f8c8d);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* 框架样式 */
QFrame {
    background-color: #ffffff;
    border-radius: 8px;
}

QFrame[frameShape="1"] { /* StyledPanel */
    border: 2px solid #e1e8ed;
    padding: 10px;
}

/* 消息框样式 */
QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    font-size: 10pt;
    color: #2c3e50;
    margin: 10px;
}

QMessageBox QPushButton {
    min-width: 90px;
    padding: 8px 16px;
    margin: 5px;
}

/* 工具提示样式 */
QToolTip {
    background-color: #34495e;
    color: #ecf0f1;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 9pt;
}

/* 特殊按钮样式 - 用于不同类型的按钮 */
QPushButton#dangerButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #e74c3c, stop: 1 #c0392b);
}

QPushButton#dangerButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #ec7063, stop: 1 #e74c3c);
}

QPushButton#dangerButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #a93226, stop: 1 #922b21);
}

QPushButton#successButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #27ae60, stop: 1 #229954);
}

QPushButton#successButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #52be80, stop: 1 #27ae60);
}

QPushButton#successButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #1e8449, stop: 1 #196f3d);
}

/* 进度条样式（如果需要） */
QProgressBar {
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    background-color: #f0f3f7;
    height: 20px;
    text-align: center;
    color: #2c3e50;
    font-weight: 500;
}

QProgressBar::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 #3498db, stop: 1 #2ecc71);
    border-radius: 4px;
    margin: 1px;
}

/* 复选框样式 */
QCheckBox {
    spacing: 8px;
    color: #34495e;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #3498db;
}

QCheckBox::indicator:checked {
    background-color: #3498db;
    border-color: #2980b9;
}

QCheckBox::indicator:checked:hover {
    background-color: #2980b9;
    border-color: #21618c;
}

/* 单选按钮样式 */
QRadioButton {
    spacing: 8px;
    color: #34495e;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #bdc3c7;
    border-radius: 9px;
    background-color: #ffffff;
}

QRadioButton::indicator:hover {
    border-color: #3498db;
}

QRadioButton::indicator:checked {
    background-color: #3498db;
    border-color: #2980b9;
}



/* 状态标签样式 */
QLabel#statusLabel {
    font-size: 11pt;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
}

QLabel#statusHint {
    font-size: 9pt;
    color: #7f8c8d;
    font-style: italic;
}

QLabel#controlHint {
    font-size: 9pt;
    color: #5d6d7e;
    background-color: #eef2f7;
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 4px solid #3498db;
    margin-bottom: 5px;
}

QLabel#statusIndicator {
    font-size: 10pt;
    font-weight: 500;
    color: #27ae60;
    padding: 4px 8px;
    background-color: #d5f4e6;
    border-radius: 4px;
}

/* 主要按钮样式 */
QPushButton#primaryButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #2ecc71, stop: 1 #27ae60);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    font-size: 11pt;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #58d68d, stop: 1 #2ecc71);
}

QPushButton#primaryButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #239b56, stop: 1 #1e8449);
}

QPushButton#primaryButton:disabled {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #a9dfbf, stop: 1 #85c1a3);
    color: #ffffff;
}

"""
