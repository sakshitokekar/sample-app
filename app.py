# Flask app entry point
from flask import Flask
from routes.auth import auth_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    return app

# WHO: Agent 2 (Dev Agent)
# WHAT: Configured Flask app to bind to host '0.0.0.0' and disabled debug mode.
# WHY: To make the Flask app reachable from outside the Docker container in Kubernetes and remove the security risk of the interactive debugger (SDLC-13).
# WHEN: 2026-08-28T14:30:00.000000
# WHERE: app.py __main__
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=False, port=5000)
