from src.api.app import create_app
from src.settings.settings import ProdConfig

app = create_app(ProdConfig)
