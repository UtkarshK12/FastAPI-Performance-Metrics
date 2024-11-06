# How to run

## setup (only one time)
1. create virtual env using "python3.10 -m venv venv"
2. activate it "source ./venv/bin/activate"
3. install dependencies "pip install -r requirements.txt"


## run the app
1. run "cd app && uvicorn main:app --reload"
2. in a new terminal run this "curl http://localhost:8000/test/sample"