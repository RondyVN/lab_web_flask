from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField, FileAllowed


class CreatePostForm(FlaskForm):
    title = email = StringField('Title', validators=[DataRequired(), Length(min=1)])
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('type', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
