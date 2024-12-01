from flask import *
import pymysql

app = Flask(__name__)

@app.route('/') 
def home(): 
    return render_template("index.html")

@app.route('/menu')   
def menu():
    return render_template("menu.html")

@app.route('/place_order')   
def place_order():
    return render_template("place_order.html") 

@app.route('/cart')   
def cart():
    return render_template("cart.html")

@app.route("/uploadnew" , methods=["POST","GET"])
def uploadnew():
    if request.method == "GET":
     return render_template("uploadnew.html")
    else:
        foodname = request.form ["foodname"]
        description = request.form ["description"]
        price = request.form ["price"]
        image_name = request.files ["image_name"]
        image_name.save("static/foods/" + image_name.filename)

        connection = pymysql.connect(host="localhost" , user="root" , password="" ,database="keroma")

        sql = "INSERT INTO `menu_items`( `foodname`, `description`, `price`, `image_name`) VALUES (%s, %s, %s, %s)"

        cursor = connection.cursor()
        cursor.execute(sql, (foodname, description, price, image_name.filename))
        
        connection.commit()
        return render_template("uploadnew.html", message =" Uploaded Succesfully")
    

app.run(debug=True)