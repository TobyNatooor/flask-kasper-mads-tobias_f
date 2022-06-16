# imports
from flask import Flask, render_template, request, redirect, url_for, session
import sql

Sql = sql.SqlClass('./static/db/TogWebsiteSQL.db')

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Endpoints
@app.route('/')
def home():
    session["numberOfItems"] = len(Sql.getCart())
    return render_template('home.html', trainData=Sql.GetTrainData())

@app.route('/reviews')
def reviews():
    trainID = request.args.get('trainID')
    trainData = Sql.getTrainDataByID(trainID)
    print(trainData)
    train = {
        "name": trainData[0][0],
        "price": trainData[0][3],
        "image": trainData[0][2],
    }
    return render_template('reviews.html', train=train)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html', methods=["Get", "POST"])

@app.route('/login-form', methods=["Get", "POST"])
def loginForm():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            enteredPassword = request.form.get("password")
            passwordIsCorrect = Sql.isCorrectPassword(username, enteredPassword)
            if passwordIsCorrect:
                session["username"] = username
            else:
                error = "Dit login var usuccesful"
                return redirect(url_for("login", errorMessage=error))
        except:
            error = "Du er ikke oprettet i vores database\nGå ind på registrer og opret dig"
            return redirect(url_for("login", errorMessage=error))
    return redirect(url_for("home"))

@app.route('/register-form', methods=["Get", "POST"])
def registerForm():
    if request.method == "POST":
        try:
            Username = request.form.get("username")
            tlf = request.form.get("tlf")
            email = request.form.get("email")
            password = request.form.get("password")
            error = ""
            if not len(Username) > 5:
                error = "Username er forkert minimum 5 lang"
            if not tlf.isdecimal() == True:
                error = "Dette er ikke et tlf nummer!"
            if not "@" in email and "." in email:
                error = "Dette er ikke en gyldig email"
            if not len(password) > 5:
                error = "Lav et bedre password #SkillIssue"

            if error == "":
                Sql.registerUser(Username, tlf, email, password)
            else:
                return redirect(url_for("login", errorMessage=error))
        except:
            return redirect(url_for("login", errorMessage="fejl i login"))
    return redirect(url_for("home"))

@app.route('/buy-form', methods=["Get", "POST"])
def buyForm():
    if request.method == "POST":
        trainID = request.form.get("trainID")
        Sql.addToCart(trainID)
    return redirect(url_for("home"))

def getCartData():
    cartTrainData = []
    for id in Sql.getCart():
        trainData = Sql.getTrainDataByID(id[0])
        cartTrainData.append({
            "name": trainData[0][0],
            "price": trainData[0][3],
            "image": trainData[0][2],
            "ID": trainData[0][1],
        })
    return cartTrainData

def getCartSum():
    cartData = getCartData()
    trainPriceSum = 0
    for trainData in cartData:
        trainPriceSum += trainData["price"]
    return trainPriceSum

@app.route('/cart')
def cart():
    return render_template('cart.html', cartTrainData=getCartData(), trainPriceSum=getCartSum())

@app.route('/remove-item', methods=["POST"])
def removeItem():
    if request.method == "POST":
        trainID = request.form.get("trainID")
        Sql.deleteCartItemById(trainID)
    return render_template('cart.html', cartTrainData=getCartData(), trainPriceSum=getCartSum())

if __name__ == '__main__':
    app.run()
