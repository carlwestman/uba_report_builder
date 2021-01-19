import contextlib
import OpenSSL.crypto
import requests
import tempfile
from datetime import datetime
import zipfile
import pandas as pd
from models.sector import Sector
from app import db, app
# -*- coding: utf-8 -*-


@contextlib.contextmanager
def pfx_to_pem(pfx_path, pfx_password):
    ''' Decrypts the .pfx file to be used with requests. '''
    with tempfile.NamedTemporaryFile(suffix='.pem') as t_pem:
        f_pem = open(t_pem.name, 'wb')
        pfx = open(pfx_path, 'rb').read()
        p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
        f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
        f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
        ca = p12.get_ca_certificates()
        if ca is not None:
            for cert in ca:
                f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        f_pem.close()
        yield t_pem.name


def get_comp_reg(url, pfx_path, pfx_pw):
    """
    downloads sekto file from SCB, returns path to unziped txt file
    :param url:
    :param pfx_path:
    :param pfx_pw:
    :return:
    """
    with pfx_to_pem(pfx_path, pfx_pw) as cert:
        response = requests.get(url, cert=cert)
        zip_cont = response.content
    base_store_path = 'data/foretags_register/ftg_reg_'+datetime.strftime(datetime.today(), '%Y-%m-%d')
    zip_store_path = base_store_path + '.zip'
    store_path = base_store_path
    with open(zip_store_path, "wb") as f:
        f.write(zip_cont)
    with zipfile.ZipFile(zip_store_path, 'r') as zip_file:
        zip_file.extractall(store_path)
    return store_path + '/sektor.txt'


def comp_reg_to_sql(file_loc):

    ftg_pd = pd.read_csv(file_loc, sep="\t", encoding="iso-8859-1")
    col_names = ["IdNr", "OrgNr", "Name", "SectorCode", "Sector", "Industry", "IndustryCode", "IndustryCode2",
                 "OwnerCategoryCode", "OwnerCategory", "LegalFormCode", "LegalForm"]
    ftg_pd.columns = col_names
    ftg_pd['IdNr'] = ftg_pd['IdNr'].astype(str)
    sectors_df = ftg_pd.to_dict(orient='index')
    for s in sectors_df:
        sector_entry = Sector(
            IdNr=sectors_df[s]["IdNr"],
            OrgNr=sectors_df[s]["OrgNr"],
            Name=sectors_df[s]["Name"],
            SectorCode=sectors_df[s]["SectorCode"],
            Sector=sectors_df[s]["Sector"],
            Industry=sectors_df[s]["Industry"],
            IndustryCode=sectors_df[s]["IndustryCode"],
            IndustryCode2=sectors_df[s]["IndustryCode2"],
            OwnerCategoryCode=sectors_df[s]["OwnerCategoryCode"],
            OwnerCategory=sectors_df[s]["OwnerCategory"],
            LegalForm=sectors_df[s]["LegalForm"],
            LegalFormCode=sectors_df[s]["LegalFormCode"]
        )
        db.session.add(sector_entry)
    db.session.commit()


def update_company_register(file_loc=None):
    if not file_loc:
        file_loc = get_comp_reg(app.config["SCB_URL"], app.config["PFX_CERT_PATH"], app.config["PFX_PASSWORD"])
    comp_reg_to_sql(file_loc)
