import os

from app import create_app

app = create_app()

# run the application
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
