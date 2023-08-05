DISCORD_API_BASE_URL = "https://discordapp.com/api"

DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + "/oauth2/authorize"
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + "/oauth2/token"


DISCORD_OAUTH_ALL_SCOPES = [
    "bot", "connections", "email", "identify", "guilds", "guilds.join",
    "gdm.join", "messages.read", "rpc", "rpc.api", "rpc.notifications.read", "webhook.incoming",
]

DISCORD_OAUTH_DEFAULT_SCOPES = [
    "identify", "email", "guilds", "guilds.join"
]


DISCORD_IMAGE_BASE_URL = "https://cdn.discordapp.com/"
DISCORD_IMAGE_FORMAT = "png"
DISCORD_ANIMATED_IMAGE_FORMAT = "gif"
DISCORD_USER_AVATAR_BASE_URL = DISCORD_IMAGE_BASE_URL + "avatars/{user_id}/{avatar_hash}.{format}"
DISCORD_GUILD_ICON_BASE_URL = DISCORD_IMAGE_BASE_URL + "icons/{guild_id}/{icon_hash}.png"
