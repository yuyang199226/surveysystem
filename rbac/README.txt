主要功能

使用说明
settings 配置常量
配置的常量中以KEY结尾的值都可以是任意数值

# ############################## RBAC权限相关配置开始 
# session中保存权限信息的Key
RBAC_PERMISSION_URL_SESSION_KEY = "rbac_permission_url_session_key"

# Session中保存菜单和权限信息的Key
RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
RBAC_MENU_KEY = "rbac_menu_key"
RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"

# 匹配URL时指定规则
RBAC_MATCH_PARTTERN = "^{0}$"

# 无需权限控制的URL
RBAC_NO_AUTH_URL = [
    '/login/',
    "/index/",
]
# 无权访问时，页面提示信息
RBAC_PERMISSION_MSG = "无权限访问"

# 菜单主题
RBAC_THEME = "default"
# ############################## RBAC权限相关配置结束 #########################

rbac 下middleware.rbac 写的中间件类。需要加入到settings 的中间件列表的末尾。
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middleware.rbac.RbacMiddleware'
]




