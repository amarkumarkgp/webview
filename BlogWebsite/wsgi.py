import os
from application import create_app


base_dir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.path.join(base_dir, 'settings.py'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
