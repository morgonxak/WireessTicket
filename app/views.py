from app import app
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import json

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        infoUser = {}
        #Всегда отправляет то дальше не пускам
        infoUser['phone'] = request.form['phone']
        infoUser['password'] = request.form['password']
        #Если они пришли то отправить стоимоть проезда
        infoUser['magor'] = request.form['magor']
        infoUser['minor'] = request.form['minor']
        #писание средств
        infoUser['transaction'] = request.form['transaction']
        if authentication(infoUser['phone'], infoUser['password']):
            res = app.config['db'].getDataBus(infoUser['minor'], infoUser['magor'])
            jsonData = {'price': res[0][1]}
        else:
            jsonData = {'Error': 'authentication'}

        if infoUser['transaction'] != None:
            if authentication(infoUser['phone'], infoUser['password']):
                wallet = app.config['db'].getDataPeopleWallet(infoUser['phone'], infoUser['password'])[0][0]
                if wallet - float(infoUser['transaction']) >= 0:
                    app.config['db'].payment(infoUser['phone'], infoUser['password'], infoUser['transaction'])
                    jsonData = {'transaction': True, 'wallet': wallet - float(infoUser['transaction'])}
                else:
                    jsonData = {'transaction': False, 'wallet': wallet}

        response = app.response_class(
            response=json.dumps(jsonData),
            status=200,
            mimetype='application/json'
        )
        return response

    return render_template("main.html")

def authentication(phone, password):

    if len(app.config['db'].getDataPeopleWallet(str(phone), str(password))) != 0:
        return True
    else:
        return False
