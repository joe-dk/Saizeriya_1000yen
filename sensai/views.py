from flask import request, redirect, url_for, render_template, flash
from sensai import app, db
from sensai.models import Menu
import random

@app.route('/')
def show_menus():
    return render_template('show_menus.html')

@app.route('/get', methods=['GET'])
def get_menus():

    # params
    menus = []
    text = "サイゼリヤ1000円ガチャを回したよ！" + "\n" + "\n"
    money = 1000
    budget = money
    calorie = 0
    salt = 0

    # select first food
    while not menus:
        rand = random.randrange(0, db.session.query(Menu.id).count()) + 1
        menus = db.session.query(Menu).filter(Menu.id==rand, Menu.price <= budget).all()

    # calc
    budget -= int(menus[0].price)
    calorie += int(menus[0].calorie)
    salt += float(menus[0].salt)

    #add text for tweet
    text += str(menus[0].name) + "\n"

    while budget > 0:

        # avalable food candidate
        candidate = db.session.query(Menu).filter(Menu.price <= budget).all()

        # no candidate break
        if not candidate:
            break

        # select food
        rand = random.randrange(0, len(candidate))

        # add to list
        menus.append(candidate[rand])

        #add text for tweet
        text += str(candidate[rand].name) + "\n"

        #calc
        budget -= int(candidate[rand].price)
        calorie += int(candidate[rand].calorie)
        salt += float(candidate[rand].salt)


    budget = money - budget

    # tweet result
    text += "\n"
    text += "計 " + str(budget) + "円 " + str(calorie) + "kcal 塩分 " + str(round(salt,1)) + "g" + "\n" + "\n"

    return render_template('show_menus.html', menus=menus, budget=budget, calorie=calorie, salt=round(salt,1), text=text)

import random
