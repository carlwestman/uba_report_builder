from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class UploadFileForm(FlaskForm):
    balance_date = DateField(validators=[DataRequired()])
    file = FileField(validators=[DataRequired()])
    submit = SubmitField('Ladda upp fil')


class ChooseCompareFileForm(FlaskForm):
    file = SelectField(validators=[DataRequired()])
    submit = SubmitField('Välj fil')
