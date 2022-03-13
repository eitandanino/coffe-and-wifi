from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

now = datetime.now()


class CafeShops(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


# #WTForm
class CreatePostForm(FlaskForm):
    name = StringField("Caffe Name", validators=[DataRequired()])
    img_url = StringField("Image url", validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Do they have sockets?")
    has_toilet = BooleanField("Do they have bathrooms?")
    has_wifi = BooleanField("Do they have wifi")
    can_take_calls = BooleanField("Can you talk there?")
    seats = StringField("How many seats", validators=[DataRequired()])
    coffee_price = StringField("What is the coffee price", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route("/")
def home_page():
    cafes = CafeShops.query.all()
    return render_template("index.html", now=now, cafes=cafes)


@app.route("/all_caffe_shops")
def all_shops():
    cafes = CafeShops.query.all()
    return render_template("show_all_shops.html", now=now, cafes=cafes)


@app.route("/shop/<int:shop_id>")
def show_shop(shop_id):
    requested_shop = CafeShops.query.get(shop_id)
    return render_template("shop.html", shop=requested_shop, now=now)


@app.route('/new_post', methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_shop = CafeShops(
            name=form.name.data,
            img_url=form.img_url.data,
            map_url=form.map_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,

        )
        db.session.add(new_shop)
        db.session.commit()
        return redirect(url_for("home_page"))
    return render_template("new_shop.html", form=form, now=now)


@app.route("/edit_shop/<int:shop_id>", methods=["GET", "POST"])
def edit_shop(shop_id):
    shop = CafeShops.query.get(shop_id)
    edit_form = CreatePostForm(
        name=shop.name,
        img_url=shop.img_url,
        map_url=shop.map_url,
        location=shop.location,
        has_sockets=shop.has_sockets,
        has_toilet=shop.has_toilet,
        has_wifi=shop.has_wifi,
        can_take_calls=shop.can_take_calls,
        seats=shop.seats,
        coffee_price=shop.coffee_price,

    )
    if edit_form.validate_on_submit():
        shop.name = edit_form.name.data,
        shop.img_url = edit_form.img_url.data,
        shop.map_url = edit_form.map_url.data,
        shop.location = edit_form.location.data,
        shop.has_sockets = edit_form.has_sockets.data,
        shop.has_toilet = edit_form.has_toilet.data,
        shop.has_wifi = edit_form.has_wifi.data,
        shop.can_take_calls = edit_form.can_take_calls.data,
        shop.seats = edit_form.seats.data,
        shop.coffee_price = edit_form.coffee_price.data,
        db.session.commit()
        return redirect(url_for("show_shop", shop_id=shop.id))
    return render_template("new_shop.html", is_edit=True, form=edit_form, now=now)


@app.route('/delete/<int:shop_id>')
def delete_post(shop_id):
    post_to_delete = CafeShops.query.get(shop_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run(debug=True)
