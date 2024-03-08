from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL
import csv
from csv import writer




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), URL(require_tld=True, message="must be a valid URL")])
    open_time = StringField('Open time', validators=[DataRequired()])
    close_time = StringField('Close time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee', choices=['☕️','☕️☕️','☕️☕️☕️','☕️☕️☕️☕️','☕️☕️☕️☕️☕️'], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi', choices=['✘','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'], validators=[DataRequired()])
    power_rating = SelectField('Power', choices=['✘','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'], validators=[DataRequired()])

    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    name = form.cafe.data
    location = form.location_url.data
    open_time = form.open_time.data
    close_time = form.close_time.data
    coffee_rating = form.coffee_rating.data
    wifi_rating = form.wifi_rating.data
    power_rating = form.power_rating.data
    list_to_add = [name, location, open_time, close_time, coffee_rating, wifi_rating, power_rating]
    print(list_to_add)
    if form.validate_on_submit():
        # row items: Cafe Name,Location,Open,Close,Coffee,Wifi,Power
        print("True")
        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow("")
            writer_object.writerow(list_to_add)
            # Close the file object
            f_object.close()

        return cafes()
    else:
        print("False")
        print(list_to_add)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
