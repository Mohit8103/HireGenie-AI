import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    app.run()

