from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.automap import automap_base
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, URLField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config["SECRET_KEY"] = "123"


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    Base = automap_base()
    Base.prepare(autoload_with=db.engine)
    cafe = Base.classes.cafe


class Add_Cafe_Form(FlaskForm):
    name = StringField(validators=[DataRequired()])
    map_url = URLField(validators=[DataRequired()])
    img_url = URLField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])

    seats = StringField(validators=[DataRequired()])
    coffee_price = StringField(validators=[DataRequired()])

    has_wifi = BooleanField(validators=[DataRequired()])
    has_toilet = BooleanField(validators=[DataRequired()])
    has_sockets = BooleanField(validators=[DataRequired()])
    can_take_calls = BooleanField(validators=[DataRequired()])

    submit = SubmitField(validators=[DataRequired()])


@app.route("/")
def home():
    data = db.session.execute(db.select(cafe)).scalars()
    year = datetime.now().year
    return render_template("index.html", data=data, year=year)


@app.route("/add_cafe", methods=['GET', 'POST'])
def add_cafe():
    form = Add_Cafe_Form()
    if form.validate_on_submit():
        new_cafe = cafe(name=form.name.data, map_url=form.map_url.data, img_url=form.img_url.data,
                        location=form.location.data, coffee_price=form.coffee_price.data, seats=form.seats.data,
                        has_wifi=form.has_wifi.data, has_sockets=form.has_sockets.data, has_toilet=form.has_toilet.data,
                        can_take_calls=form.can_take_calls.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route('/delete_cafe/<int:cafe_id>', methods=['GET', 'POST'])
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5002)
