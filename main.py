from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location URL', validators=[DataRequired(), URL(True)])
    open_time = TimeField('open time', validators=[DataRequired()])
    closing_time = TimeField('closing time', validators=[DataRequired()])
    coffee_rate = SelectField('coffee rating', choices=[
        ('0', '✘'),
        ('1', '☕️'),
        ('2', '☕️☕️'),
        ('3', '☕️☕️☕️'),
        ('4', '☕️☕️☕️☕️'),
        ('5', '☕️☕️☕️☕️☕️')
    ], validators=[DataRequired()])
    wifi_rate = SelectField('wifi rating', choices=[
        ('0', '✘'),
        ('1', '💪'),
        ('2', '💪💪'),
        ('3', '💪💪💪'),
        ('4', '💪💪💪💪'),
        ('5', '💪💪💪💪💪')
    ], validators=[DataRequired()])
    power_rate = SelectField('power outlet rating',  choices=[
        ('0', '✘'),
        ('1', '🔌'),
        ('2', '🔌🔌'),
        ('3', '🔌🔌🔌'),
        ('4', '🔌🔌🔌🔌'),
        ('5', '🔌🔌🔌🔌🔌')
    ], validators=[DataRequired()])
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


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
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


@app.route('/add', methods=["POST"])
def add():
    add_form = CafeForm()
    if add_form.validate_on_submit():
        with open('cafe-data.csv', 'a', encoding='utf-8', ) as csv_file:
            new_line = (f'\n{add_form.cafe.data},'
                        f'{add_form.location.data},'
                        f'{add_form.open_time.data}, '
                        f'{add_form.closing_time.data},'
                        f'{add_form.coffee_rate.choices[int(add_form.coffee_rate.data)][1]},'
                        f'{add_form.wifi_rate.choices[int(add_form.wifi_rate.data)][1]},'
                        f'{add_form.power_rate.choices[int(add_form.power_rate.data)][1]}')
            csv_file.write(new_line)
        with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                list_of_rows.append(row)
        return render_template('cafes.html', cafes=list_of_rows)
    return render_template('add.html', form=add_form)


if __name__ == '__main__':
    app.run(debug=True)
