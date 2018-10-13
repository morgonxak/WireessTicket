from app import app
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import json

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        a = False
        b = False
        c = False

        infoUser = {}
        #Всегда отправляет то дальше не пускам
        try:
            infoUser['phone'] = request.form['phone']
            infoUser['password'] = request.form['password']

            if str(infoUser['phone']) != "" and str(infoUser['password']) != "":
                a = True
        except BaseException:
            pass


        #Если они пришли то отправить стоимоть проезда
        try:
            infoUser['magor'] = request.form['magor']
            infoUser['minor'] = request.form['minor']
            if str(infoUser['magor']) != "" and str(infoUser['minor']) != "":
                b = True
            else:
                raise BaseException
        except BaseException:
            pass
        #Cписание средств
        try:
            infoUser['transaction'] = request.form['transaction']
            if len(str(infoUser['transaction'])) > 0:
                c = True
        except BaseException:
            pass

#Если пришли только phone, password
        if a and authentication(infoUser['phone'], infoUser['password']):
            info = app.config['db'].getUserInfo(infoUser['phone'], infoUser['password'])
            jsonData = {'firstname': info[0][0], 'lastname': info[0][1], 'wallet': info[0][2], 'phone': info[0][3]}
        else:
            jsonData = {'Error': 'login'}

#Если пришли только phone, password, minor, magor
        if a and b and authentication(infoUser['phone'], infoUser['password']):
            res = app.config['db'].getDataBus(infoUser['minor'], infoUser['magor'])
            #info = app.config['db'].getUserInfo(infoUser['phone'], infoUser['password'])
            #[('Дмитрий', 'Шумелев', 977.0, 79994318576)]
            #jsonData = {'firstname': info[0][0], 'lastname': info[0][1], 'wallet': info[0][2], 'phone': info[0][3], 'price': res[0][1]}
            jsonData = {'price': res[0][1]}
        else:
            pass
            #jsonData = {'Error': 'authentication'}

# Если пришли только phone, password, transaction
        if a and c:
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
