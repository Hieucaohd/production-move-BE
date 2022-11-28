from dotenv import load_dotenv
load_dotenv()

from src.api.app import create_app
from src.settings.settings import DevConfig

if __name__ == '__main__':
    CONFIG = DevConfig
    app = create_app(CONFIG)
    app.run(debug=True)
