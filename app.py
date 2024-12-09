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


def get_access_token():
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = base64.b64encode(f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}

    response = requests.get(auth_url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("access_token")
    else:
        print(f"Error getting access token: {response.text}")  # Log the error for debugging
        raise Exception("Failed to get access token from M-Pesa")


@app.route("/stkpush", methods=["POST"])
def stkpush():
    try:
        # Validate request payload
        data = request.json
        phone_number = data.get("phoneNumber")
        amount = data.get("amount")

        if not phone_number or not amount:
            return jsonify({"success": False, "message": "Phone number and amount are required"}), 400

        # Generate access token
        access_token = get_access_token()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        password = base64.b64encode(
            f"{MPESA_SHORTCODE}{passkey}{timestamp}".encode()
        ).decode()

        # Prepare STK Push payload
        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": phone_number,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Cart Checkout",
            "TransactionDesc": "Payment for cart items",
        }

        # Send STK Push request
        response = requests.post(stk_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("ResponseCode") == "0":
            return jsonify({"success": True, "message": "STK push initiated"}), 200
        else:
            print(f"STK push failed: {response.text}")  # Log error for debugging
            return jsonify({"success": False, "message": response_data.get("errorMessage", "STK push failed")}), 400

    except Exception as e:
        print(f"Error in /stkpush: {e}")  # Log exception for debugging
        return jsonify({"success": False, "message": "Internal server error"}), 500


@app.route("/simulate-payment/<transaction_id>", methods=["GET"])
def simulate_payment(transaction_id):
    # Simulate payment confirmation
    from random import choice
    success = choice([True, False])  # Randomly simulate success or failure
    if success:
        return jsonify({"success": True, "transactionId": transaction_id})
    else:
        return jsonify({"success": False, "transactionId": transaction_id})



if __name__ == "__main__":
    app.run(debug=True)
