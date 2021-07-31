from app import create_app, create_db

app, manager = create_app(__name__)

if __name__ == "__main__":
    # with app.app_context():
    #    create_db()
    app.run(debug=True)