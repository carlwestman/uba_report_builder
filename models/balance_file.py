from app import db


class BalanceFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(100), nullable=False)
    BalanceDate = db.Column(db.Date, nullable=False)
    NrEntries = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'FileName: {self.FileName} BalanceDate: {self.BalanceDate}, NrEntries: {self.NrEntries}'
