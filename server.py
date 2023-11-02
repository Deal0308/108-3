from flask import Flask, request
from config import me
from mock_data import catalog
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


@app.get("/api/catalog")
def get_catalog():
    return json.dumps(catalog)


@app.post('/api/catalog')
def save_product():
    product = request.get_json()

    product['_id'] = len(catalog)
    catalog.append(product)

    return json.dumps(product)


# create a get /api/report/total
# that send the total value of your catalog (sum of all prices)
@app.get("/api/report/total")
def get_report_total():
    total = 0
    for prod in catalog:
        total += prod['price']
    return json.dumps({"total": total})   

# get all products for a given category
# get /api/catalog/cat/<category>
# get /api/catalog/cat/Fruit
@app.get("/api/products/<cat>")
def get_by_category(cat):
    results = []
    for prod in catalog:
        if prod["category"] == cat:
            results.append(prod)
    return json.dumps(results)


app.run(debug=True)

# get search <term>

@app.get("/api/products/search/<term>")
def product_search(term):
    results = []
    for prod in catalog:
        if term.lower() in prod["title"].lower():
            results.append(prod)
    return json.dumps(results)


