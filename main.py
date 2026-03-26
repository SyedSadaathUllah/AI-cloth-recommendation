from flask import Flask, render_template, request
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Dataset (5 features: occasion, weather, style, height, skin)
data = [
    [0,0,0,0,0],
    [0,0,1,1,1],
    [1,0,0,2,0],
    [1,1,1,0,2],
    [0,1,0,1,1],
    [1,1,1,2,2],
    [0,0,1,1,0],
    [1,0,0,2,1]
]

labels = [
    "casual_hot_simple",
    "casual_hot_stylish",
    "party_hot_simple",
    "party_cold_stylish",
    "casual_cold_simple",
    "party_cold_stylish",
    "casual_hot_stylish",
    "party_hot_simple"
]

# Outfit mapping
outfit_map = {
    "casual_hot_simple": {
        "upper": "tshirt",
        "lower": "shorts",
        "footwear": "slippers",
        "accessory": "cap"
    },
    "casual_hot_stylish": {
        "upper": "oversized tshirt",
        "lower": "cargo shorts",
        "footwear": "sneakers",
        "accessory": "sunglasses"
    },
    "party_hot_simple": {
        "upper": "shirt",
        "lower": "jeans",
        "footwear": "loafers",
        "accessory": "watch"
    },
    "party_cold_stylish": {
        "upper": "leather jacket",
        "lower": "black jeans",
        "footwear": "boots",
        "accessory": "watch"
    },
    "casual_cold_simple": {
        "upper": "hoodie",
        "lower": "jeans",
        "footwear": "sneakers",
        "accessory": "beanie"
    }
}

# Train model
model = LogisticRegression()
model.fit(data, labels)

@app.route("/", methods=["GET", "POST"])
def index():
    outfit = None

    if request.method == "POST":
        occasion = request.form["occasion"]
        weather = request.form["weather"]
        style = request.form["style"]
        height = request.form["height"]
        skin = request.form["skin"]

        # Encode
        o = 0 if occasion == "casual" else 1
        w = 0 if weather == "hot" else 1
        s = 0 if style == "simple" else 1

        h_map = {"short":0, "average":1, "tall":2}
        s_map = {"light":0, "medium":1, "dark":2}

        h = h_map[height]
        sk = s_map[skin]

        prediction = model.predict([[o, w, s, h, sk]])
        outfit_type = prediction[0]

        outfit = outfit_map.get(outfit_type, {
            "upper": "tshirt",
            "lower": "jeans",
            "footwear": "shoes",
            "accessory": "watch"
        })

    return render_template("index.html", outfit=outfit)


if __name__ == "__main__":
    app.run(debug=True)