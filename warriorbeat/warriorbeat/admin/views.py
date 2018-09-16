# warriorbeat/admin/views.py


import requests
from flask import Blueprint, Flask, json, jsonify, redirect, render_template, \
    request, url_for
from werkzeug.utils import secure_filename
import tempfile
import os
import datetime
from slugify import slugify
from .forms import AddFeedForm, EmailForm


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
        img = form.cover_img.data
        img_name = img.filename
        # date = datetime().now()
        slug = slugify(form.title.data)
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'wb') as tmp:
            img.save(tmp)
            tmp.close()
        data = {
            'feedId': form.id.data,
            'title': form.title.data,
            'author': form.author.data,
            'body': form.body.data,
            # 'slug': slug,
            # 'date': 'today',
            'cover_img': path
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url_for('feedlist', _external=True),
                          data=json.dumps(data), headers=headers)
        os.remove(path)
        return redirect(url_for('admin.home'))
    return render_template('home/add_feed.html', form=form)
