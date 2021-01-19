from app import db


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(100), nullable=False)
    BalanceDate = db.Column(db.Date, nullable=False)
    LoanNumber = db.Column(db.Integer, nullable=False)
    Applicant = db.Column(db.String(12), nullable=False)
    CoApplicant = db.Column(db.String(12), nullable=True)
    CollateralType = db.Column(db.Integer, nullable=False)
    NominalOutstandingAmount = db.Column(db.Float, nullable=False)
    CurrentValuation = db.Column(db.Float, nullable=False)
    RiskClass = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'BalanceDate: {self.BalanceDate}Loan: {self.LoanNumber}, ' \
               f'Collateral: {self.CollateralType}, Nom.Outstanding: {self.NominalOutstandingAmount}'
