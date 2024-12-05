from flask import *
import pymysql

app = Flask(__name__)

@app.route('/') 
def home(): 
    return render_template("index.html")

@app.route('/menu')   
def menu():
    connection = pymysql.connect(host="localhost", user='root', password='', database='keroma')

    # fetch electronics 
    sql1 = 'select * from menu_items'
    cursor = connection.cursor()
    cursor.execute(sql1)
    menu_items = cursor.fetchall()
    
    return render_template("menu.html", menu_items = menu_items)

@app.route('/cart')   
def cart():
    return render_template("cart.html")

@app.route('/carttrial')   
def carttrial():
    return render_template("carttrial.html")

@app.route("/upload" , methods=["POST","GET"])
def upload():
    if request.method == "GET":
     return render_template("upload.html")
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
        return render_template("upload.html", message =" Uploaded Succesfully")
    

app.run(debug=True)