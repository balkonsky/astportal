from flask import Flask, render_template_string
from flask_wtf import Form
from wtforms import FieldList, StringField

app = Flask(__name__)
app.secret_key = 'TEST'


class TestForm(Form):
    person = FieldList(StringField('Person'), min_entries=3, max_entries=10)
    foo = StringField('Test')
    name = StringField('name')


@app.route('/process_add_member', methods=['POST'])
def add_member():
    pass


@app.route('/form')
def main_form():
    pass


@app.route('/', methods=['POST', 'GET'])
def example():
    form = TestForm()
    if form.validate_on_submit():
        print(form.person.data)

    return render_template_string(
        """
            <script type="text/javascript">

    $("#add-member").on('click', function(event){
        $.ajax({
            url: "{{ url_for('add_member') }}",
            type : "POST",
            //dataType : 'json', // data type
            data : $("#main-form").serialize(),
            success : function(result) {
                console.log(result);
                $("#members").html(result);
            },
            error: function(xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        });
        event.preventDefault();

        });
</script>


<form method="post" action="{{ url_for('main_form') }}" id="main-form">
{{ form.hidden_tag() }}
{{ form.name.label }} {{ form.name }}


<fieldset class="form-group border p-2">
    <span id="members">{% include 'members.html' %}</span>

    <div class="form-row">
        {{ form.add_member(id="add-member") }}
    </div>
</fieldset>

</form>
        """, form=form)


if __name__ == '__main__':
    app.run(debug=True)
