from flask import Flask
from config import me
import json


app = Flask(__name__)

@app.get("/")
def index():
    return "Hello, World!"



@app.get("/test")
def test():
    return "this is another page"


# ######################################################################   API   ######################################################################


@app.get("/api/version")
def version():
    v = {
        "version": "1.0.0",
        "name": "Genesis"
    }
    return json.dumps(v)

# get /api/about
#  return the me dictionary as json
@app.get("/api/about")
def about():
    return json.dumps(me)

app.run(debug=True)

