# warriorbeat/admin/views.py

from flask import Flask, Blueprint, render_template, redirect, url_for, request, json, jsonify
from .forms import EmailForm, AddFeedForm
import requests

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')


@admin.route('/')
def home():
    return render_template('home/home.html')


@admin.route('/test', methods=["post", "get"])
def test():
    form = EmailForm()
    if form.validate_on_submit():
        print(form)
        return redirect(url_for('admin.home'))
    return render_template('home/test.html', form=form)


@admin.route('/add', methods=["post", "get"])
def add_feed():
    form = AddFeedForm()
    if form.validate_on_submit():
        print(url_for('api.create_feed'))
        print('FORM INFO')
        data = {
            'feedId': request.form['id'],
            'name': request.form['name']
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url_for('api.create_feed', _external=True),
                          data=json.dumps(data), headers=headers)

        return redirect(url_for('admin.home'))
    return render_template('home/add_feed.html', form=form)
