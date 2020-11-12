# 命名正则(包含（豆瓣中文）标题和年份，默认为电影名、中文括号年份)
MOVIE_DIR_RE = '(.*?)（(\d{4})）'

# 启用Telegram推送
TG_ON = False

# telegram chat id（群组、频道、或用户）
TG_CHAT_ID = 123456

# telegram bot token
TG_BOT_TOKEN = ''

# 启用友盟推送
UMENG_ON = False
UMENG_APPKEY = ''
UMENG_SECRET = ''

# 启用Bark(IOS)推送
BARK_ON = False

# Bark Token列表
BARK_TOKENS = ['',]

# API Token
API_TOKEN = 'qecdsf2sds'

# 代理(对Telegram生效)
PROXY = False
PROXY_URL = 'http://127.0.0.1:7890'

# App播放链接(配合LocalMovieDB, 如http://xxx.xx/movie/dbid/, 留空则不显示)
APP_PAGE = ''
