��Ҫ����

ʹ��˵��
settings ���ó���
���õĳ�������KEY��β��ֵ��������������ֵ

# ############################## RBACȨ��������ÿ�ʼ 
# session�б���Ȩ����Ϣ��Key
RBAC_PERMISSION_URL_SESSION_KEY = "rbac_permission_url_session_key"

# Session�б���˵���Ȩ����Ϣ��Key
RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
RBAC_MENU_KEY = "rbac_menu_key"
RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"

# ƥ��URLʱָ������
RBAC_MATCH_PARTTERN = "^{0}$"

# ����Ȩ�޿��Ƶ�URL
RBAC_NO_AUTH_URL = [
    '/login/',
    "/index/",
]
# ��Ȩ����ʱ��ҳ����ʾ��Ϣ
RBAC_PERMISSION_MSG = "��Ȩ�޷���"

# �˵�����
RBAC_THEME = "default"
# ############################## RBACȨ��������ý��� #########################

rbac ��middleware.rbac д���м���ࡣ��Ҫ���뵽settings ���м���б��ĩβ��
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




