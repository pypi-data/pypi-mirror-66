from dash_infra import KWSSuperApp
from werkzeug.serving import run_simple

try:
    from .app import dash_app
except:
    from app import dash_app

super_app = KWSSuperApp({"multiplier": dash_app},)

if __name__ == "__main__":
    super_app.cli()
