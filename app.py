from flask import Flask, render_template, request, jsonify
import pymysql
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Define the directory where uploaded images will be saved
UPLOAD_FOLDER = 'static/foods'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/') 
def home(): 
    return render_template("index.html")

@app.route('/menu')   
def menu():
    connection = pymysql.connect(host="localhost", user='root', password='', database='keroma')
    try:
        # Fetch menu items
        sql1 = 'SELECT * FROM menu_items'
        cursor = connection.cursor()
        cursor.execute(sql1)
        menu_items = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template("menu.html", menu_items=menu_items)

@app.route('/cart', methods=['GET', 'POST'])   
def cart():
    if request.method == 'POST':
        # Get the JSON data sent from the frontend
        cart = request.get_json()
        print(cart)  # Debug output
        # Process cart data as needed
        return jsonify({'message': 'Cart received successfully!', 'cart': cart}), 200

    # For GET request, render the cart page
    return render_template("cart.html")

@app.route('/carttrial')   
def carttrial():
    return render_template("carttrial.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        # Get form data
        foodname = request.form["foodname"]
        description = request.form["description"]
        price = request.form["price"]
        
        # Handle image upload
        image_name = request.files["image_name"]
        if image_name:
            filename = secure_filename(image_name.filename)
            image_name.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ''

        connection = pymysql.connect(host="localhost", user="root", password="", database="keroma")
        try:
            sql = "INSERT INTO `menu_items`(`foodname`, `description`, `price`, `image_name`) VALUES (%s, %s, %s, %s)"
            cursor = connection.cursor()
            cursor.execute(sql, (foodname, description, price, filename))
            connection.commit()
            message = "Uploaded successfully!"
        except Exception as e:
            connection.rollback()
            message = f"Error uploading: {str(e)}"
        finally:
            connection.close()

        return render_template("upload.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
