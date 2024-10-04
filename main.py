# main.py

# from flask import Flask
from scraper import start_scheduler
from models import init_db
from api import create_app

def main():
    init_db()
    start_scheduler()
    
    app = create_app()
    return app

if __name__ == "__main__":
    app = main()
    app.run(host="0.0.0.0", port=5000, debug=True)