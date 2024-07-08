from app import create_app
import os

config_name = "development"

app = create_app()

if __name__ == '__main__':
    app.run(port=8090,debug=True)