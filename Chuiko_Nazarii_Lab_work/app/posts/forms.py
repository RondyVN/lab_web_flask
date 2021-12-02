from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text', validators=[Length(max=1500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('type', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    enabled = BooleanField('Enabled',)
    category = SelectField(u'Category', coerce=int)
    submit = SubmitField('Submit')
