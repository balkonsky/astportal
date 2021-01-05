from flask import Flask, render_template_string
from flask_wtf import Form
from wtforms import FieldList, StringField
from wtforms import (
    StringField,
    BooleanField,
    TextAreaField,
    FieldList,
    SubmitField,
    FormField
)

app = Flask(__name__)
app.secret_key = 'TEST'


@app.route("/modifywps", methods=['POST', 'GET'])
def modifywps():
    application_standard_id = request.args.get('std')  # gets value from the getJson()

    # process it however you want..

    return  # whatever you want.


@app.route("/newqualification/<welder_id>", methods=['GET', 'POST'])
def newqualification(welder_id=None):
    form =  # passformhere

    # writemethod.

    return render_template('xyz.html', title='xyz', form=form)


if __name__ == '__main__':
    app.run(debug=True)
