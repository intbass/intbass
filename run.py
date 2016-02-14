import logging
from app import app

if __name__ == '__main__':
    logging.basicConfig()
    app.run(debug=True)
