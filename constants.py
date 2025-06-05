"""
应用程序常量定义
统一管理所有配置常量、错误消息、UI文本等
"""

# 应用程序信息
APP_NAME = "B站答题助手"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "一个帮助B站用户自动完成答题任务的工具"

# 窗口配置
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_TITLE = APP_NAME

# 日志配置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 模型配置
MODEL_TYPES = {
    'DEEPSEEK': 'deepseek',
    'GEMINI': 'gemini',
    'CUSTOM': 'custom'
}

MODEL_DISPLAY_NAMES = {
    'deepseek': 'DeepSeek',
    'gemini': 'Gemini',
    'custom': '自定义模型'
}

MODEL_CHOICE_VALUES = {
    'deepseek': '1',
    'gemini': '2',
    'custom': '3'
}

# 默认API配置
DEFAULT_API_CONFIGS = {
    'deepseek': {
        'base_url': 'https://api.deepseek.com',
        'model': 'deepseek-chat'
    },
    'gemini': {
        'base_url': 'https://generativelanguage.googleapis.com',
        'model': 'gemini-pro'
    },
    'custom': {
        'base_url': 'https://dashscope.aliyuncs.com',
        'model': 'qwen-turbo'
    }
}

# UI文本
UI_TEXTS = {
    'LOGIN_STATUS_LOGGED_IN': '登录状态：已登录',
    'LOGIN_STATUS_NOT_LOGGED_IN': '登录状态：未登录',
    'LOGIN_BUTTON': '登录B站',
    'SWITCH_ACCOUNT_BUTTON': '切换账号',
    'START_QUIZ_BUTTON': '开始答题',
    'STOP_QUIZ_BUTTON': '停止答题',
    'LOG_TITLE': '答题日志:',
    'MODEL_SELECTION_TITLE': '选择AI模型:',
    'API_KEY_LABEL': 'API Key:',
    'API_URL_LABEL': 'API 基础URL:',
    'MODEL_NAME_LABEL': '模型名称:',
    'SAVE_SETTINGS_BUTTON': '保存设置',
    'QR_LOGIN_TITLE': 'B站扫码登录',
    'QR_LOGIN_HINT': '请使用哔哩哔哩APP扫描二维码登录',
    'QR_WAITING': '等待扫码...',
    'CAPTCHA_TITLE': '验证码',
    'CAPTCHA_CATEGORY_HINT': '请选择以下分类ID:',
    'CAPTCHA_INPUT_HINT': '输入验证码:',
    'CAPTCHA_ID_INPUT_HINT': '输入分类ID (多个ID用英文逗号隔开):'
}

# 错误消息
ERROR_MESSAGES = {
    'NOT_LOGGED_IN': '请先登录B站账号',
    'API_KEY_MISSING': '请先在设置中配置{model}API密钥',
    'LOGIN_FAILED': '登录失败，请重试',
    'LOGOUT_FAILED': '登出失败，无法切换账号',
    'QUIZ_START_ERROR': '答题启动失败',
    'MODEL_CONFIG_ERROR': '模型配置错误',
    'NETWORK_ERROR': '网络连接错误',
    'CAPTCHA_LOAD_ERROR': '加载验证码失败',
    'CAPTCHA_DISPLAY_ERROR': '显示验证码失败',
    'QR_CODE_GENERATE_ERROR': '生成二维码失败'
}

# 成功消息
SUCCESS_MESSAGES = {
    'LOGIN_SUCCESS': '登录成功',
    'LOGOUT_SUCCESS': '已登出当前账号',
    'SETTINGS_SAVED': '{model}设置已保存',
    'ACCOUNT_SWITCHED': '新账号登录成功',
    'QUIZ_STARTED': '开始使用{model}模型答题...',
    'QUIZ_STOPPED': '答题已停止',
    'QUIZ_FINISHED': '答题已结束',
    'VERIFICATION_PASSED': '验证通过✅'
}

# 信息消息
INFO_MESSAGES = {
    'PREPARING_LOGIN': '正在准备B站登录...',
    'SWITCHING_ACCOUNT': '正在切换账号...',
    'GETTING_CATEGORIES': '获取分类信息...',
    'GETTING_CAPTCHA': '获取验证码...',
    'SHOWING_CAPTCHA_DIALOG': '显示验证码输入对话框，验证码链接: {url}',
    'SHOWING_CATEGORY_DIALOG': '显示验证码分类选择对话框...',
    'STOPPING_QUIZ': '正在停止答题...',
    'QUIZ_ALREADY_STOPPED': '答题已停止'
}

# 线程超时设置
TIMEOUTS = {
    'CAPTCHA_WAIT': 30,  # 验证码等待超时（秒）
    'LOGIN_WAIT': 60,    # 登录等待超时（秒）
    'NETWORK_REQUEST': 10  # 网络请求超时（秒）
}

# 文件路径
PATHS = {
    'CONFIG_DIR': 'config',
    'LOG_DIR': 'logs',
    'TEMP_DIR': 'temp',
    'GUI_ERROR_LOG': 'logs/gui_error.log'
}

# 验证码图片设置
CAPTCHA_SETTINGS = {
    'MAX_WIDTH': 400,
    'MIN_HEIGHT': 100,
    'LOAD_TIMEOUT': 10
}

# 二维码设置
QR_CODE_SETTINGS = {
    'VERSION': 1,
    'BOX_SIZE': 5,
    'BORDER': 2,
    'DISPLAY_SIZE': 200
}

# 阿里云DashScope提示信息
DASHSCOPE_TIPS = """阿里云DashScope提示:
基础URL: https://dashscope.aliyuncs.com
模型: qwen-turbo, qwen-plus 或 llama3-8b-chat"""

# 关于页面HTML内容
ABOUT_HTML = """
<h2 style="text-align: center;">B站答题助手</h2>
<p style="text-align: center;">一个帮助B站用户自动完成答题任务的工具</p>
<p><b>功能特点:</b></p>
<ul>
    <li>支持使用多种AI模型</li>
    <li>支持DeepSeek、Gemini和自定义模型</li>
    <li>支持阿里云通义千问等API</li>
    <li>现代化GUI界面</li>
</ul>
<p><b>使用说明:</b></p>
<ol>
    <li>在"设置"标签页配置API密钥和模型</li>
    <li>在"首页"登录B站账号</li>
    <li>点击"开始答题"按钮开始自动答题</li>
</ol>
<p><b>注意事项:</b></p>
<ul>
    <li>使用前请确保已配置正确的API密钥</li>
    <li>程序仅调用B站接口和LLM API，不会上传个人信息</li>
    <li>如果使用Gemini，注意需要切换至Gemini允许的地区运行</li>
</ul>
""" 