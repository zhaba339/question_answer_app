from authx import AuthX
from authx import AuthX, AuthXConfig

config = AuthXConfig()
security = AuthX(config=config)

config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]