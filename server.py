from flask import Flask, request, abort
from config import me
from mock_data import catalog, coupon_codes
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

@app.get("/api/products/lower/<price>")
def get_lower(price):
    results = []
    for prod in catalog:
        if prod["price"] <= float(price):
            results.append(prod)
    return json.dumps(results)


######################################################################   COUPON   ######################################################################

@app.get("/api/coupon_codes")
def get_coupon_codes():
    return json.dumps(coupon_codes)

# post /api/coupon_codes


# save a coupon
@app.post("/api/coupon_codes")
def save_coupon():
    coupon = request.get_json()
    coupon["_id"] = len(coupon_codes)

    coupon_codes.append(coupon)
    return json.dumps(coupon)

# get /api/coupons/apply/<code>
# search for the coupon with the code
# return the obj/dict if exist

@app.get("/api/coupons/<code>")
def search_coupon(code):
    for coupon in coupon_codes:
        if coupon["code"].lower() == code.lower():
            return json.dumps(coupon)
    return abort(404, "Invalid code")
# get /api/coupons/apply/<code>/<price>
# search for the coupon with the code
# if exist, calculate the discount
# return the obj/dict if exist

@app.get("/api/coupons/apply/<code>/<price>")
def apply_coupon(code, price):
    for coupon in coupon_codes:
        if coupon["code"] == code:
            discount = float(price) * coupon["discount"]
            return json.dumps({"discount": discount})
    return json.dumps({"error": True, "message": "Invalid code"})


