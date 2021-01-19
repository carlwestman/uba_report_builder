import openpyxl
import pandas as pd
from sqlalchemy import text

from app import db


def make_report(new_file_name, balance_date, new_file_id=None, compare_file=None):
    query = text(f"""
    SELECT * FROM
        (
        SELECT a. *, b.sector 
        FROM loan a left outer join sector b on a.Applicant = b.IdNr
        UNION ALL
        SELECT a. *, b.sector
        FROM loan a INNER JOIN sector b on a.CoApplicant = b.IdNr)
        WHERE
        FileName = '{new_file_name}'
    """
                 )
    in_data = pd.read_sql(query, con=db.engine, )
    in_data["sector"].fillna(value="Övriga Hushåll", inplace=True)

    R = Report(in_data, balance_date)
    return_obj = {
        'report_result': "Success",
        'report_result_msg': 'Rapporten har skapats!',
        'directory': R.output_loc,
        'filename': R.output_filename}
    return return_obj


class Report:

    def __init__(self, data, balance_date):
        self.data = data
        self.balance_date = balance_date
        self.output_filename = 'UBA-' + self.balance_date.strftime('%Y-%m-%d') + '.txt'
        self.output_loc = 'data/reports/'
        self.output_file = open(self.output_loc+self.output_filename, 'w')
        self.keys = {
            "ftg_hh": "Företagarhushåll utan anställda",
            "o_hh": "Övriga Hushåll",
            "hh_iv_org": "Hushållens icke-vinstdrivande organisationer, utom registrerade trossamfund",
            "h": "house",
            "b": "brf"
        }
        self.spec_t3_sektor = self.mk_spec_t3_sektor(data)
        self.spec_t3_sakerhet_loptid = self.mk_spec_t3_sakerhet_loptid(data)
        self.spec_t3_nodlidande_lan = self.mk_spec_t3_nodlidande_lan(data)
        self.kopta_och_salda_lan = {
            'sheet': 'Köpta_och_sålda_lån',
            'data': [
                {'cell': '321A_A_M2C_X_V1EN_X_1E_N1221391_V_B_A', 'value': 0},
                {'cell': '321A_A_M2C_X_V1EN3_X_1E_N1221391_V_B_A', 'value': 0},
                {'cell': '321A_A_M2C_X_V1EN311_X_1E_N1221391_V_B_A', 'value': 0},
                {'cell': '321A_A_M2C_X_V1EN311_4B_1E_N1221391_V_B_A', 'value': 0},
                {'cell': '321A_A_M2C_X_V1EN312_X_1E_N1221391_V_B_A', 'value': 0},
                {'cell': '321A_A_M2C_X_V1EN312_4B_1E_N1221391_V_B_A', 'value': 0}]
        }  # TODO WHEN NECESSARY
        self.omvardering_spec_t3_motp = {
            'sheet': 'Omvärderingar_Spec_T3_Motp',
            'data': [
                {'cell': '41_A_M2C_X_X_X_5J_N_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_X_1E_N_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_X_1E_N3_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_X_1E_N311_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_X_1E_N312_SEK_B_A', 'value': 0},
            ]
        }  # TODO WHEN NECESSARY
        self.omvardering_spec_t3_saker = {
            'sheet': 'Omvärderingar_T3_Säkerh',
            'data': [
                {'cell': '41_A_M2C_X_X_4D_1E_N311_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_B_1E_N311_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_4D_1E_N312_SEK_B_A', 'value': 0},
                {'cell': '41_A_M2C_X_X_B_1E_N312_SEK_B_A', 'value': 0},
            ]
        }  # TODO WHEN NECESSARY

        self.sheets_data = [
            self.spec_t3_sektor,
            self.spec_t3_sakerhet_loptid,
            self.spec_t3_nodlidande_lan,
            self.kopta_och_salda_lan,
            self.omvardering_spec_t3_motp,
            self.omvardering_spec_t3_saker
            ]
        for sheet_data in self.sheets_data:
            self.template_data(sheet_data)

        self.output_file.write('\n')
        self.output_file.close()


    @staticmethod
    def zero_if_missing(series, keys):
        val = series
        for key in keys:
            try:
                val = val[key]
            except KeyError:
                val = 0
                break
        return val

    def mk_spec_t3_sektor(self, data):
        loan_per_sect = data.groupby(by=["sector"])["NominalOutstandingAmount"].sum()

        return {
            'sheet': 'Spec_T3_Sektor',
            'data': [
                {
                    'cell': '5_A_M2C_X_X_X_1E_N3_SEK_B_A',
                    'value': data["NominalOutstandingAmount"].sum()
                },
                {
                    'cell': '5_A_M2C_X_X_X_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [self.keys["ftg_hh"]])
                },
                {
                    'cell': '5_A_M2C_X_X_X_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [self.keys["o_hh"]])
                },
                {
                    'cell': '5_A_M2C_X_X_X_1E_N32_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [self.keys["hh_iv_org"]])
                }
            ]
        }

    def mk_spec_t3_sakerhet_loptid(self, data):
        loan_per_sect_coll = data.groupby(by=["sector", "CollateralType"])["NominalOutstandingAmount"].sum()

        return {
            'sheet': 'Spec_T3_Säkerhet_löptid',
            'data': [{
                'cell': '5_A_M2C_X_X_4D_1E_N311_SEK_B_A',
                'value': self.zero_if_missing(loan_per_sect_coll, [
                    self.keys["ftg_hh"],
                    self.keys["h"]
                ])},
                {
                    'cell': '5_A_M2C_RY_X_4D_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["ftg_hh"],
                        self.keys["h"]
                    ])},
                {
                    'cell': '5_A_M2C_X_X_B_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["ftg_hh"],
                        self.keys["b"]
                    ])},
                {
                    'cell': '5_A_M2C_RY_X_B_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["ftg_hh"],
                        self.keys["b"]
                    ])},
                {
                    'cell': '5_A_M2C_X_X_4D_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["o_hh"],
                        self.keys["h"]
                    ])},
                {
                    'cell': '5_A_M2C_RY_X_4D_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["o_hh"],
                        self.keys["h"]
                    ])},
                {
                    'cell': '5_A_M2C_X_X_B_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["o_hh"],
                        self.keys["b"]
                    ])},
                {
                    'cell': '5_A_M2C_RY_X_B_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect_coll, [
                        self.keys["o_hh"],
                        self.keys["b"]
                    ])}
            ]
        }

    def mk_spec_t3_nodlidande_lan(self, data):
        nod_lid_loan = data[data["RiskClass"] == 5]
        loan_per_sect = nod_lid_loan.groupby(
            by=["sector"])["NominalOutstandingAmount"].sum()

        loan_per_sect_coll = nod_lid_loan.groupby(
            by=["sector", "CollateralType"])["NominalOutstandingAmount"].sum()
        return {
            'sheet': 'Spec_T3_Nödlidande_lån',
            'data': [
                {
                    'cell': '5_A_M2C10_X_X_X_5J_N_SEK_B_A',
                    'value': nod_lid_loan["NominalOutstandingAmount"].sum()
                },
                {
                    'cell': '5_A_M2C10_X_X_X_1E_N_SEK_B_A',
                    'value': nod_lid_loan["NominalOutstandingAmount"].sum()
                },
                {
                    'cell': '5_A_M2C10_X_X_X_1E_N3_SEK_B_A',
                    'value': nod_lid_loan["NominalOutstandingAmount"].sum()
                },
                {
                    'cell': '5_A_M2C10_X_X_X_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [
                        self.keys["ftg_hh"]])
                },
                {
                    'cell': '5_A_M2C10_X_X_4B_1E_N311_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [
                        self.keys["ftg_hh"]])
                },
                {
                    'cell': '5_A_M2C10_X_X_X_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [
                        self.keys["o_hh"], ])},
                {
                    'cell': '5_A_M2C10_X_X_4B_1E_N312_SEK_B_A',
                    'value': self.zero_if_missing(loan_per_sect, [
                        self.keys["o_hh"], ])
                }
            ]
        }

    def template_data(self, sheet_data):

        for entry in sheet_data["data"]:
            cell = entry["cell"]
            value = entry["value"]

            row = '#R;'+str(cell)+";"+str(int(value))+'\n'
            self.output_file.write(row)
