import os
from application import create_app


base_dir = os.path.abspath(os.path.dirname(__file__))


def main():
    app = create_app(os.path.join(base_dir, 'settings.py'))
    app.app_context().push()
    # app.secret_key = "somesecretekey"
    app.run(debug=True)


if __name__ == "__main__":
    main()
