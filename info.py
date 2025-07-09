import re
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value and value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value and value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    return default

# Bot Information
SESSION = environ.get('SESSION', 'KeralaCaptain')
API_ID = int(environ.get('API_ID', '20836266'))
API_HASH = environ.get('API_HASH', 'bbdd206f92e1ca4bc4935b43dfd4a2a1')
BOT_TOKEN = environ.get('BOT_TOKEN', "")

# Bot Settings
CACHE_TIME = int(environ.get('CACHE_TIME', 1800))
PICS = (environ.get('PICS', "https://envs.sh/sxe.jpg")).split()
NOR_IMG = environ.get("NOR_IMG", "https://graph.org/file/b69af2db776e4e85d21ec.jpg")
MELCOW_VID = environ.get("MELCOW_VID", "")
SPELL_IMG = environ.get("SPELL_IMG", "https://te.legra.ph/file/15c1ad448dfe472a5cbb8.jpg")

# Admins, Channels & Users
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002462335914'))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7577977996 6644681404').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

# Force Subscribe
REQUEST_TO_JOIN_MODE = is_enabled(environ.get('REQUEST_TO_JOIN_MODE', 'True'), True)
TRY_AGAIN_BTN = is_enabled(environ.get('TRY_AGAIN_BTN', 'True'), True)
auth_channel = environ.get('AUTH_CHANNEL', '-1002449923339')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# Channels
reqst_channel = environ.get('REQST_CHANNEL_ID', '-1002493027541')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1002306779893')
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in environ.get('FILE_STORE_CHANNEL', '-1002405400154').split()]
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]

# Database
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://primemastix:o84aVniXFmKfyMwH@cluster0.qgiry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "primemastix")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'TomCollection')

# Premium & Referral
PREMIUM_AND_REFERAL_MODE = is_enabled(environ.get('PREMIUM_AND_REFERAL_MODE', 'False'), False)
REFERAL_COUNT = int(environ.get('REFERAL_COUNT', '20'))
REFERAL_PREMEIUM_TIME = environ.get('REFERAL_PREMEIUM_TIME', '1month')
PAYMENT_QR = environ.get('PAYMENT_QR', '')
PAYMENT_TEXT = environ.get('PAYMENT_TEXT', script.PAYMENT_TEXT)
OWNER_USERNAME = environ.get('OWNER_USERNAME', 'CjjTom')

# Clone Mode
CLONE_MODE = is_enabled(environ.get('CLONE_MODE', 'False'), False)
CLONE_DATABASE_URI = environ.get('CLONE_DATABASE_URI', "")
PUBLIC_FILE_CHANNEL = environ.get('PUBLIC_FILE_CHANNEL', 'KeralaPrimeMovie')

# Links
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/CJMovieSearch')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/CJMovieSearch')
TUTORIAL = environ.get('TUTORIAL', '')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'KeralaLeechHelp')

# Features
AI_SPELL_CHECK = is_enabled(environ.get('AI_SPELL_CHECK', 'True'), True)
PM_SEARCH = is_enabled(environ.get('PM_SEARCH', 'True'), True)  # Set to True as requested
IS_SHORTLINK = is_enabled(environ.get('IS_SHORTLINK', 'False'), False)
MAX_BTN = is_enabled(environ.get('MAX_BTN', 'True'), True)
IS_TUTORIAL = is_enabled(environ.get('IS_TUTORIAL', 'True'), True)
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', 'False'), False)
IMDB = is_enabled(environ.get('IMDB', 'True'), True)
AUTO_FFILTER = is_enabled(environ.get('AUTO_FFILTER', 'True'), True)
AUTO_DELETE = is_enabled(environ.get('AUTO_DELETE', 'True'), True)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', 'True'), True)
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "True"), True)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', "True"), True)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', "True"), True)
NO_RESULTS_MSG = is_enabled(environ.get("NO_RESULTS_MSG", "False"), False)
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', "True"), True)

# Verification
VERIFY = is_enabled(environ.get('VERIFY', 'False'), False)
VERIFY_SECOND_SHORTNER = is_enabled(environ.get('VERIFY_SECOND_SHORTNER', 'False'), False)
VERIFY_SHORTLINK_URL = environ.get('VERIFY_SHORTLINK_URL', '')
VERIFY_SHORTLINK_API = environ.get('VERIFY_SHORTLINK_API', '')
VERIFY_SND_SHORTLINK_URL = environ.get('VERIFY_SND_SHORTLINK_URL', '')
VERIFY_SND_SHORTLINK_API = environ.get('VERIFY_SND_SHORTLINK_API', '')
VERIFY_TUTORIAL = environ.get('VERIFY_TUTORIAL', '')

# Shortlink
SHORTLINK_MODE = is_enabled(environ.get('SHORTLINK_MODE', 'False'), False)
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
SHORTLINK_API = environ.get('SHORTLINK_API', '317e5f6ab1aa6fba5fb3623a24caf6a26f6e177e')

# Other Settings
MAX_B_TN = int(environ.get("MAX_B_TN", "5"))
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', 'ʜɪ ʙʀᴏ ᴡʜᴀᴛ s ᴜᴘ')
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", script.CAPTION)
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", script.IMDB_TEMPLATE_TXT)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)

# Search Filters
LANGUAGES = ["malayalam", "mal", "tamil", "tam", "english", "eng", "hindi", "hin", 
             "telugu", "tel", "kannada", "kan"]
SEASONS = [f"season {i}" for i in range(1, 11)]
EPISODES = [f"E{i:02d}" for i in range(1, 41)]
QUALITIES = ["360p", "480p", "720p", "1080p", "1440p", "2160p"]
YEARS = [str(year) for year in range(1900, 2026)]

# Stream Mode
STREAM_MODE = is_enabled(environ.get('STREAM_MODE', 'True'), True)
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
ON_HEROKU = 'DYNO' in environ
URL = environ.get("URL", "https://full-trixie-primeyour-13b7cc8d.koyeb.app/")

# File Handling
RENAME_MODE = is_enabled(environ.get('RENAME_MODE', 'True'), True)
AUTO_APPROVE_MODE = is_enabled(environ.get('AUTO_APPROVE_MODE', 'True'), True)

# Log Configuration
LOG_STR = "Current Configuration:\n"
LOG_STR += f"IMDB: {'Enabled' if IMDB else 'Disabled'}\n"
LOG_STR += f"P_TTI_SHOW_OFF: {'Enabled' if P_TTI_SHOW_OFF else 'Disabled'}\n"
LOG_STR += f"SINGLE_BUTTON: {'Enabled' if SINGLE_BUTTON else 'Disabled'}\n"
LOG_STR += f"CUSTOM_FILE_CAPTION: {CUSTOM_FILE_CAPTION[:50] + '...' if CUSTOM_FILE_CAPTION else 'Not Set'}\n"
LOG_STR += f"LONG_IMDB_DESCRIPTION: {'Enabled' if LONG_IMDB_DESCRIPTION else 'Disabled'}\n"
LOG_STR += f"SPELL_CHECK_REPLY: {'Enabled' if SPELL_CHECK_REPLY else 'Disabled'}\n"
LOG_STR += f"MAX_LIST_ELM: {MAX_LIST_ELM if MAX_LIST_ELM else 'No Limit'}\n"
LOG_STR += f"Current IMDB template:\n{IMDB_TEMPLATE[:200]}...\n" if IMDB_TEMPLATE else "No IMDB Template Set\n"

# Validate required configurations
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")
if not DATABASE_URI:
    raise ValueError("DATABASE_URI environment variable is required!")
