from app import app

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/data.db"
app.config['REPORT_FOLDER'] = 'data/reports/'


app.config['PFX_CERT_PATH'] = ''
app.config['PFX_PASSWORD'] = ''
app.config['SCB_URL'] = 'https://privateapi.scb.se/nv0101/v1/sokpavar/api/Je/SektorFil'
