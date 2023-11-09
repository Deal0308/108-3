from flask import Flask, request, abort
from config import me, db
from mock_data import catalog, coupon_codes
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # this will allow CORS for all routes, meaning that any frontend can make requests to this API

@app.get("/")
def index():
    return "Hello, World!"



@app.get("/test")
def test():
    return "this is another page"


# ######################################################################   API   ######################################################################

def fix_id(record):
    record["_id"] = str(record["_id"])
    return record





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
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        fix_id(prod)
        results.append(prod)
    return json.dumps(results)


@app.post('/api/catalog')
def save_product():
    product = request.get_json()

# save product to the database
    db.products.insert_one(product)

    return json.dumps(product)


# create a get /api/report/total
# that send the total value of your catalog (sum of all prices)
@app.get("/api/report/total")
def get_report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod['price']
    
    results = {
        "report": "total",
        "value": total
    }
    return json.dumps({"total": total})   

# get all products for a given category
# get /api/catalog/cat/<category>
# get /api/catalog/cat/Fruit
@app.get("/api/products/<cat>")
def get_by_cursor(cat):
    cursor = db.products.find({"category": cat})
    results = []
    for prod in cursor:
        fix_id(prod)
        results.append(prod)
    return json.dumps(results)



@app.get("/api/products/lower/<price>")
def products_lower(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({"price": {"$lt": real_price}})
    
    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)


# get price greater or equal than <price>
@app.get("/api/products/greater/<price>")
def products_greater(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({"price": {"$gte": real_price}})
    
    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)


######################################################################   COUPON   ######################################################################

@app.get("/api/coupon_codes")
def get_coupon_codes():
    cursor = db.coupon_codes.find({})
    results = []
    for coupon in cursor:
        fix_id(coupon)
        results.append(coupon)
    return json.dumps(coupon_codes)

# post /api/coupon_codes


# save a coupon
@app.post("/api/coupon_codes")
def save_coupon():
    coupon = request.get_json()
    

    coupon_codes.append(coupon)
    # save coupon to the database
    db.coupon_codes.insert_one(coupon)
    return json.dumps(coupon)

# get /api/coupons/apply/<code>
# search for the coupon with the code
# return the obj/dict if exist

@app.get("/api/coupons/<code>")
def search_coupon(code):
    coupon = db.coupons.find_one({"code": {'$regex': f"^{code}$", '$options': "i"}})
    

    if not coupon:
        return abort(404, "Invalid code")
    fix_id(coupon)
    return json.dumps(coupon)
        
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


