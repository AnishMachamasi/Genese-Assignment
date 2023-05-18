from flask import Flask, render_template, request, redirect, session, url_for, flash
from twilio.rest import Client
import requests
from database import create_database
import sqlite3
import random

app = Flask(__name__)
app.secret_key = '2262'

#display home page
@app.route('/')
def home():
    return render_template('home.html')

#displat login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #retrieve the email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        #connect to the database
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()

        # Retrieve the user with the provided email
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = c.fetchall()

        #check if the email and password matched with the registered user
        if result:
            for row in result:
                stored_password = row[4]  # Assuming password is stored at index 4 in the table
                if password == stored_password:
                    conn.close()
                    
                    # Store the email in session
                    session['email'] = email
                    
                    #if match then send the authentication code to the user via sms
                    account_sid = 'AC889ebdf1d6145f9ed2423396da006467'
                    auth_token = 'aa80404dd47daf94a34133840f3b8d8c'
                    client = Client(account_sid, auth_token)
                    
                    
                    # Generate a random authentication code
                    auth_code = str(random.randint(100000, 999999))
                    
                    #store auth code in session
                    session['auth_code'] = auth_code

                    #send message to the user
                    message = client.messages.create(
                    from_='+12542846996',
                    body=f'Authentication code: {auth_code}',
                    to='+9779860116983'
                    )
                    
                    
                    return render_template('2factorAuth.html')
        conn.close()
        return 'Invalid email or password or you didnot signed up yet!'

    return render_template('login.html')

#display signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #retrieve the data from the form
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Perform validation and processing of the sign-up data here

        #connect to the database
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()

        # Check if the email already exists in the database
        c.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        result = c.fetchone()

        if result[0] > 0:
            conn.close()
            return 'Email already exists! Just Log-In'  # Or redirect to an error page

        # Insert the user data into the database
        c.execute("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                   (username, email, phone, password))
        conn.commit()
        conn.close()

        return redirect('/login')  # Redirect to the dashboard page after successful sign-up

    return render_template('sign_up.html')

#two factor authentication verification - security
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    verification_code = request.form.get('verification_code')

    # retrieve verficication code from session store in login
    stored_auth_code = session.get('auth_code')

    if verification_code == stored_auth_code:
        return redirect('/dashboard')
    else:
        return 'Invalid verification code'
    

#display dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    url = "https://coinranking1.p.rapidapi.com/coins"

    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "3h",
        "tiers[0]": "1",
        "orderBy": "marketCap",
        "orderDirection": "desc",
        "limit": "150",
        "offset": "0"
    }

    #API keys obtained from rapidapi.com
    headers = {
        "X-RapidAPI-Key": "52ceb5a784msh9c0e480a52d97ecp1dd28ejsn40bcebde0cae",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    coins = data['data']['coins']
    coin_data = []

    #store the data in coin_data, made some changes to the data by rounding off
    for coin in coins:
        market_cap = round(float(coin['marketCap']), 2)
        price = round(float(coin['price']), 2)
        volume = round(float(coin['24hVolume']), 2)
        btc_price = round(float(coin['btcPrice']), 2)
        coin_data.append({
            'iconUrl': coin['iconUrl'],
            'name': coin['name'],
            'symbol': coin['symbol'],
            'marketCap': (market_cap),
            'price': (price),
            'change': coin['change'],
            'rank': coin['rank'],
            '24hVolume': (volume),
            'btcPrice': (btc_price)
        })
    
    #check which user is logged in and display the dashboard accordingly
    if 'email' in session:
        email = session['email']
        
        if email == "anishmachamasi2262@gmail.com": 
            return render_template('macha-dashboard.html', data=coin_data)
        elif email == "anishshilpakar@gmail.com":
            return render_template('bunty-dashboard.html', data=coin_data)
    
#display portfolio page
@app.route('/portfolio')
def portfolio():
    if 'email' in session:
        email = session['email']
        
        if email == "anishmachamasi2262@gmail.com": 
            conn = sqlite3.connect('user_info.db')
            c = conn.cursor()

            # Retrieve the sell data for non-matching emails from the database
            c.execute("SELECT symbol, coin_amount, total_price FROM sell WHERE email != ?", (email,))
            sell_data = c.fetchall()
            
            # Calculate sell_total_data
            sell_total_data = 0
            symbol =0
            coin_amount =0
            for record in sell_data:
                symbol = record[0]
                coin_amount = record[1]
                total_price = record[2]
                sell_total_data += coin_amount * total_price

            # Delete the sell data records for non-matching emails
            c.execute("DELETE FROM sell WHERE email != ?", (email,))
            conn.commit()

            conn.close()
            
            return render_template('macha-portfolio.html', sell_total_data=sell_total_data, symbol=symbol, total_coin=coin_amount)
        elif email == "anishshilpakar@gmail.com":
            
            conn = sqlite3.connect('user_info.db')
            c = conn.cursor()

            # Retrieve the sell data for non-matching emails from the database
            c.execute("SELECT symbol, coin_amount, total_price FROM sell WHERE email != ?", (email,))
            sell_data = c.fetchall()
            
            # Calculate sell_total_data
            sell_total_data = 0
            symbol = 0
            coin_amount = 0
            for record in sell_data:
                symbol = record[0]
                coin_amount = record[1]
                total_price = record[2]
                sell_total_data += coin_amount * total_price

            # Delete the sell data records for non-matching emails
            c.execute("DELETE FROM sell WHERE email != ?", (email,))
            conn.commit()

            conn.close()
            return render_template('bunty-portfolio.html', sell_total_data=sell_total_data, symbol=symbol, total_coin=coin_amount)
        else:
            return "Access denied!"

    return redirect(url_for('login'))

#store the order in the buy and sell database
@app.route('/store_order', methods=['POST'])
def store_order():
    email = session['email']
    symbol = request.form.get('symbol')
    coin_amount = request.form.get('coinAmount')
    total_price = request.form.get('totalPrice')
    transaction_type = request.form.get('transactionType')

    # Store the order data in the database or perform any other necessary actions
    if transaction_type == 'buy':
        # Insert buy information into the buy table
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute("INSERT INTO buy (Email, symbol,coin_amount, total_price) VALUES (?, ?, ?, ?)",
                    (email, symbol, coin_amount, total_price))
        conn.commit()
        conn.close()
        flash('Your buy order has been placed successfully!')
        
    elif transaction_type == 'sell':
        # Insert sell information into the sell table
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute("INSERT INTO sell (Email, symbol, coin_amount, total_price) VALUES (?, ?, ?, ?)",
                    (email, symbol, coin_amount, total_price))
        conn.commit()
        conn.close()
        flash('Your sell order has been placed successfully!')

    return redirect('/dashboard')


if __name__ == '__main__':
    #create database and tables if they donot exist
    create_database()
    
    #run the app in debug mode
    app.run(debug=True)
