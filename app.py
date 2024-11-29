from flask import *
import pymysql

app = Flask(__name__)

@app.route('/') 
def home(): 
    return render_template("index.html")

@app.route('/menu')   
def menu():
    return render_template("menu.html") 

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

        sql = "INSERT INTO menu-items ( 'foodname', 'description', 'price', 'image_name') VALUES (%s, %s, %s, %s)"

        cursor = connection.cursor()
        cursor.execute(sql, (foodname, description, price, image_name.filename))
        
        connection.commit()
        return render_template("upload.html", message =" Uploaded Succesfully")
    

app.run(debug=True)