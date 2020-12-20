# run.py

import os

from app import create_app

config_name = os.environ.get("KEEMAIL_ENV") or 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
