from app import app
from flask import render_template, request, send_from_directory, current_app
from src.fileHandler import import_file_content
from src.reportMaker import make_report
import forms
import os


@app.route('/history', methods=["GET"])
def history():
    return render_template('history.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.UploadFileForm()
    data = {}
    if form.validate_on_submit():
        data = import_file_content(request.form["balance_date"],
                                   request.files["file"])
        if data["upload_result"] == 'Success':
            report = make_report(data['uploaded_file_name'], data["balance_date"])
            data["report_result"] = report['report_result']
            data["report_result_msg"] = report['report_result_msg']
            data["report_directory"] = report['directory']
            data["report_filename"] = report['filename']
    return render_template('index.html', form=form, data=data)


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['REPORT_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


""" Removed the option to 
@app.route("/compare", methods=['GET', 'POST'])
def compare():
    uploaded_file = request.args.get('new_file')
    uploaded_file_obj = BalanceFile.query.filter_by(FileName=uploaded_file).first()
    uploaded_file_id = uploaded_file_obj.id
    files = [(b.id, b.BalanceDate.strftime("%Y-%m-%d") + " - " + b.FileName)
             for b in BalanceFile.query.order_by('FileName')]
    form = forms.ChooseCompareFileForm()
    form.file.choices = files

    data = {
        "result": None,
        "result_msg": None,
        "uploaded_file": uploaded_file,
        "uploaded_file_id": uploaded_file_id
    }
    if form.validate_on_submit():
        compare_file_id = request.form["file"]
        report = make_report(uploaded_file, uploaded_file_id, compare_file_id)
        data["result"] = "Success"
        data["result_msg"] = "Woot Woot report is cumming man!"

    return render_template('compare.html', form=form, data=data)
"""
