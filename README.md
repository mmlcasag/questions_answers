# To create a virtual environent for the project:
python3 -m venv env

# To activate the created virtual environment:
source env/bin/activate

# To install Flask inside the virtual environment:
pip install flask

# Environment variables for the project:
export FLASK_APP=app.py
export FLASK_DEBUG=1

# To run the project:
flask run

# To start the database:
sqlite3 database/questions_answers.db < database/questions_answers.sql
