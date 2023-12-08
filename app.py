from flask import Flask

app = Flask(__name__)

stores = [
    {
        "name" : "My Wonderful Store",
        "items" : [
            {
                "name" : "First Item",
                "price" : 750
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores" : stores}