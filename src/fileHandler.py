import pandas as pd
from models.loan import Loan
from models.balance_file import BalanceFile
from app import db
from datetime import datetime
import time
from sqlalchemy.exc import SQLAlchemyError


def import_file_content(balance_date, file):
    file_name = str(int(time.time())) + "_" + file.filename
    file_loc = "data/balance_reports/" + file_name
    file.save(file_loc)
    rows_df = pd.read_csv(file_loc, na_filter=False)
    rows_df["Applicant"] = rows_df["Applicant"].astype(str)
    rows_dict = rows_df.to_dict(orient="index")
    balance_date = datetime.strptime(balance_date, '%Y-%m-%d')
    nr_entries = len(rows_dict)

    B = BalanceFile(
        FileName=file_name,
        BalanceDate=balance_date,
        NrEntries=nr_entries
    )

    db.session.add(B)

    for i in rows_dict:
        loan = Loan(FileName=file_name,
                    BalanceDate=balance_date,
                    LoanNumber=rows_dict[i]["LoanNumber"],
                    Applicant=str(rows_dict[i]["Applicant"]),
                    CoApplicant=str(rows_dict[i]["CoApplicant"]),
                    CollateralType=rows_dict[i]["CollateralType"],
                    NominalOutstandingAmount=float(rows_dict[i]["NominalOutstandingAmount"]),
                    CurrentValuation=float(rows_dict[i]["CurrentValuation"]),
                    RiskClass=rows_dict[i]["RiskClass"])

        db.session.add(loan)

    return_data = {
        "upload_result": None,
        "upload_result_msg": None,
        "uploaded_file_name": file_name,
        "nr_entries": nr_entries,
        "balance_date": balance_date
    }
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return_data["upload_result"] =  "Error"
        return_data["upload_result_msg"] = str(e.__dict__["orig"])

    return_data["upload_result"] = "Success"
    return_data["upload_result_msg"] = f'Succé! En fil med {nr_entries} rader laddades upp!'
    return return_data
