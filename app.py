from flask import Flask, render_template, request, jsonify
import pymysql
import os

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
            # Fetch cart items with prices
            query = """
                SELECT cart.foodname, cart.quantity, menu_items.price, 
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


if __name__ == "__main__":
    app.run(debug=True)
