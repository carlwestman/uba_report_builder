from app import db


class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    IdNr = db.Column(db.String(12), nullable=False)
    OrgNr = db.Column(db.Integer, nullable=True)
    Name = db.Column(db.String(128), nullable=True)
    SectorCode = db.Column(db.Integer, nullable=False)
    Sector = db.Column(db.String(128), nullable=True)
    Industry = db.Column(db.Integer, nullable=False)
    IndustryCode = db.Column(db.Float, nullable=True)
    IndustryCode2 = db.Column(db.String(128), nullable=True)
    OwnerCategoryCode = db.Column(db.Integer, nullable=False)
    OwnerCategory = db.Column(db.String(128), nullable=True)
    LegalFormCode = db.Column(db.Integer, nullable=False)
    LegalForm = db.Column(db.String(128), nullable=True)
