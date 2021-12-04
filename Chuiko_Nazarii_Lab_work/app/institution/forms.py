from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class AddInstForm(FlaskForm):
    name_inst = StringField('Name institution', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text', validators=[Length(max=1500)])
    count_student = IntegerField('Count student', validators=[DataRequired()])
    city = StringField('City', validators=[InputRequired(), Length(min=2, max=60)])
    military_department = BooleanField(label=('Military department'))
    category = SelectField(u'Category', coerce=int)
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired(), Length(min=0, max=60)])
    submit = SubmitField('')
