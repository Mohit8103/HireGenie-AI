from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception:
        pass

if __name__ == "__main__":
    app.run()

