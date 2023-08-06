import json
from collections import defaultdict
from typing import Dict
import click

from flask import Blueprint, Flask, jsonify, render_template, request
from slugify import slugify
from werkzeug.middleware.dispatcher import DispatcherMiddleware


class KWSSuperApp:
    def __init__(self, dash_router: Dict[str, "KWSDashApp"], *args, **kwargs):
        self.app = Flask(__name__, *args, **kwargs)
        self.api = Blueprint("API", __name__, url_prefix="/api/")
        self.router = dash_router
        self.api_endpoints = defaultdict(dict)

        self.register_callbacks_as_api()

    def register_slug(self, name):
        slug = slugify(name)
        return f"/{slug}/"

    def register_callbacks_as_api(self):
        for app in self.router.values():
            for callback in app.api_callbacks:
                if hasattr(callback, "_json"):
                    self.register_api(callback)

    def register_api(self, callback):
        slug = slugify(callback.func.__name__)
        route = self.register_slug(callback.func.__name__)

        def wrapped_function():
            payload = request.form or json.loads(request.json)
            result = callback.json(**payload)
            return jsonify(result), 200

        def wrapped_doc():
            doc = {"docstring": callback.func.__doc__}

            return jsonify(doc), 200

        wrapped_function.__name__ = f"{slug}_worker"
        wrapped_doc.__name__ = f"{slug}_doc"
        self.api.route(route, methods=("POST",))(wrapped_function)
        self.api.route(route, methods=("GET",))(wrapped_doc)
        self.api_endpoints[callback.name] = callback.description

        return callback

    def create_app(self):
        self.app.register_blueprint(self.api)

        @self.app.route("/")
        def index():
            print(self.api_endpoints)
            return render_template(
                "index.html", router=self.router, endpoints=self.api_endpoints
            )

        for route, dash_app in self.router.items():
            dash_app.instanciate(
                __name__, server=self.app, routes_pathname_prefix=f"/{route}/",
            )
        return self.app

    @property
    def cli(self):
        @click.command()
        @click.option(
            "--name", "-n", required=True, type=click.Choice(self.router.keys())
        )
        @click.option("--debug", "-d", is_flag=True)
        def run_app(name, debug):
            app = self.router[name].instanciate()
            app.run_server(debug=debug)

        @click.command()
        @click.option("--debug", "-d", is_flag=True)
        def run(debug):
            app = self.create_app()
            app.run(debug=debug)

        return click.Group("run", {"run_app": run_app, "run": run})
