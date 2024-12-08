from flask import Flask, render_template, request, jsonify
import pymysql
import requests
import base64
import datetime
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
CALLBACK_URL = os.getenv("CALLBACK_URL")

app = Flask(__name__)

# Define the directory where uploaded images will be saved
UPLOAD_FOLDER = 'static/foods'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database connection function
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="keroma",
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/menu')
def menu():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch menu items
            cursor.execute("SELECT * FROM menu_items")
            menu_items = cursor.fetchall()
    finally:
        connection.close()

    return render_template("menu.html", menu_items=menu_items)


@app.route('/cart', methods=['GET'])
def cart():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch cart items with prices and images
            query = """
                SELECT 
                    cart.foodname, 
                    cart.quantity, 
                    menu_items.price, 
                    menu_items.image_name,  -- Include the image URL
                    (cart.quantity * menu_items.price) AS total_price
                FROM cart
                INNER JOIN menu_items ON cart.foodname = menu_items.foodname
            """
            cursor.execute(query)
            cart_items = cursor.fetchall()

            # Calculate grand total
            grand_total = sum(item['total_price'] for item in cart_items)
    finally:
        connection.close()

    # Pass the image URL along with other details to the template
    return render_template("cart.html", cart_items=cart_items, grand_total=grand_total)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    foodname = data['foodname']
    action = data['action']

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the current quantity
            cursor.execute("SELECT quantity FROM cart WHERE foodname = %s", (foodname,))
            result = cursor.fetchone()

            if result:
                quantity = result['quantity']
                if action == 'add':
                    quantity += 1
                elif action == 'remove' and quantity > 1:
                    quantity -= 1
                else:
                    # Remove item from cart if quantity is 0
                    cursor.execute("DELETE FROM cart WHERE foodname = %s", (foodname,))
                    connection.commit()
                    return jsonify({'message': 'Item removed', 'cart': []}), 200

                # Update the cart
                cursor.execute(
                    "UPDATE cart SET quantity = %s WHERE foodname = %s",
                    (quantity, foodname),
                )
            else:
                # Add new item to cart
                cursor.execute(
                    "INSERT INTO cart (foodname, quantity) VALUES (%s, %s)",
                    (foodname, 1),
                )

            connection.commit()

            # Fetch updated cart items
            cursor.execute("SELECT * FROM cart")
            cart_items = cursor.fetchall()
    finally:
        connection.close()

    return jsonify({'message': 'Cart updated', 'cart': cart_items}), 200


# Get Access Token
def get_access_token():
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = base64.b64encode(f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(auth_url, headers=headers)
    return response.json()["access_token"]

# STK Push
@app.route("/stkpush", methods=["POST"])
def stkpush():
    data = request.json
    phone_number = data["phoneNumber"]
    amount = data["amount"]

    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{MPESA_SHORTCODE}bfb279f9aa9bdbcf158e97dd71a467cd2d6783832c088ca11a03c073e0af9c73{timestamp}".encode()
    ).decode()

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "Cart Checkout",
        "TransactionDesc": "Payment for cart items",
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return jsonify(response.json())

# Simulated Payment Confirmation
@app.route("/payment-status/<transaction_id>", methods=["GET"])
def payment_status(transaction_id):
    # Simulate payment confirmation
    from random import randint
    if randint(0, 1):  # Simulate success 50% of the time
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


if __name__ == "__main__":
    app.run(debug=True)
