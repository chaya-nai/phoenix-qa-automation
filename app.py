from flask import Flask, Response, render_template, request, jsonify
import random

app = Flask(__name__)

character = {
    "name": "Phoenix",
    "level": 1,
    "coin": 500,
    "owned_items": [],
    "equipped_outfit": None
}

shop_items = {
    "Iron Armor": 300,
    "Leather Armor": 150,
    "Wooden Armor": 100
}

@app.route("/")
def home():
    return "Home Page"

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "status": 200,
        "message": "Server is running"
    })
    
@app.route("/api/profile", methods=['GET'])
def api_profile():
    return jsonify({
        "username": "Nai",
        "role": "QA",
        "is_active": True
    })

@app.route("/api/error", methods=["GET"])
def api_error():
    return jsonify({
        "status": 400,
        "message": "Bad Request"
    }), 400
    
@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": 503,
        "message": "Service Unavailable"
    }), 503
    
@app.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json()
    
    if "username" not in data or "password" not in data:
        return jsonify({"status": 400, "message": "Missing Credentials"}), 400
    
    if data['username'] == 'Nai' and data['password'] == '9999':
        return jsonify({"status": 200, "message": "Login Success"}), 200
    
    return jsonify({"status": 401, "message": "Invalid Credentials"}), 401

# @app.route("/login", methods=["GET","POST"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html"), 200
    
#     username = request.form['username']
#     password = request.form['password']  
#     if username == "Nai" and password == "9999":
#         text = f"Login Success \nWelcome {username}"
#         return Response(text, mimetype='text/plain'), 200

#     return "Invalid Credentials", 401

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/profile/<name>", methods=["GET"])
def profile(name):
    return f"Hello {name}"

@app.route("/api/character", methods=["GET"])
def api_character():
    return jsonify({
        "status": 200,
        "data": character
    }), 200

@app.route("/api/battle", methods=["POST"])
def api_battle():
    data = request.get_json()

    if "monster" not in data:
        return jsonify({
            "status": 400,
            "message": "Missing Monster"
        }), 400

    monster = data["monster"]

    if monster is None or monster == "":
        return jsonify({
            "status": 400,
            "message": "Invalid Monster"
        }), 400

    if monster != "Slime":
        return jsonify({
            "status": 404,
            "message": "Monster Not Found"
        }), 404

    reward = random.randint(50, 100)
    character["coin"] += reward

    return jsonify({
        "status": 200,
        "message": "Battle Won",
        "reward": reward
    }), 200

@app.route("/character")
def character_page():
    return render_template("character.html")

@app.route("/api/test/reset", methods=["POST"])
def reset_character():
    character["name"] = "Phoenix"
    character["level"] = 1
    character["coin"] = 500
    character["owned_items"] = []
    character["equipped_outfit"] = None

    return jsonify({
        "status": 200,
        "message": "Character Reset"
    }), 200

@app.route("/api/shop", methods=["GET"])
def get_shop():
    return jsonify({
        "status": 200,
        "data": shop_items
    }), 200

@app.route("/api/shop/buy", methods=["POST"])
def buy_item():
    data = request.get_json()

    if "item" not in data:
        return jsonify({
            "status": 400,
            "message": "Missing Item"
        }), 400

    item = data["item"]

    if item not in shop_items:
        return jsonify({
            "status": 404,
            "message": "Item Not Found"
        }), 404

    price = shop_items[item]

    if character["coin"] < price:
        return jsonify({
            "status": 400,
            "message": "Not Enough Coin"
        }), 400

    if item in character["owned_items"]:
        return jsonify({
            "status": 400,
            "message": "Item Already Owned"
        }), 400

    character["coin"] -= price
    character["owned_items"].append(item)

    return jsonify({
        "status": 200,
        "message": "Purchase Success",
        "item": item,
        "price": price
    }), 200
    
@app.route("/shop")
def shop_page():
    return render_template("shop.html")

@app.route("/inventory")
def inventory_page():
    return render_template("inventory.html")

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    return jsonify({
        "status": 200,
        "data": {
            "items": character["owned_items"],
            "equipped_outfit": character["equipped_outfit"]
        }
    }), 200

@app.route("/api/inventory/equip", methods=["POST"])
def equip_item():
    data = request.get_json()

    if "item" not in data:
        return jsonify({
            "status": 400,
            "message": "Missing Item"
        }), 400

    item = data["item"]

    if item not in character["owned_items"]:
        return jsonify({
            "status": 400,
            "message": "Item Not In Inventory"
        }), 400

    current_outfit = character["equipped_outfit"]

    character["owned_items"].remove(item)

    if current_outfit is not None:
        character["owned_items"].append(current_outfit)

    character["equipped_outfit"] = item

    return jsonify({
        "status": 200,
        "message": "Equip Success",
        "equipped_outfit": item
    }), 200

if __name__ == "__main__":
    app.run(debug=True)