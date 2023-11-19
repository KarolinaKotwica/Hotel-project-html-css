from flask import Flask, request, redirect
from mfchdb2 import mfchdb2
import pandas as pd
import sys
import re
from datetime import date
if sys.platform == 'zos':
    import ibm_db
    import ibm_db_dbi


def get_html_form():
    global html_form
    html_form = """
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title></title>
            <meta name="viewport" content="width=device-width initial-scale=1">
            <link rel="stylesheet" href="./static/style.css" />
        </head>
        <body>

            <div class="header">
                <div class="header_content">
                    <img class="logo" src="./static/logo.png" />
                    <div class="sitetitle">Attestation</div>
                </div>
            </div>
            <br />
            <div class="selection_container">
                <div class="selection">
                    <div class="selection_content">
    """
    return html_form


def get_PID():

    remoteuser = request.args.get('PID')

    return remoteuser

app = Flask(__name__)

@app.route("/")
def review():
    global sql
    global df

    remoteuser = get_PID()
    
    html2 = get_html_form()

    sql = """
    SELECT * FROM SAVEPROFILE
    WHERE DB_OWNER_PID = '{remoteuser}'
    """

    try:
        my_db2 = mf.mf
        df = my_db2.Db2_runsql(sql)
        my_db2 = None
    except:
        if sys.platform == "zos":
            print('exception')

    sqlSelection = """
    SELECT DB_OWNER_NAME, DB_OWNER_PID
    FROM SAVEPROFILE
    WHERE DB_OWNER_PID = '{remoteuser}'
    LIMIT 1
    """

    my_db2 = mf.mf
    dfSelection = my_db2.Db2_runsql(sql)
    my_db2 = None

    html2 += f'<table cellspacing="0" cellpadding="0" id="info"><tbody>'
    for i, row in dfSelection.iterrows():
        html2 += f"""
            <tr id='tableInfo'>
                <td><b>IT Owner:</b></td>
                <td><span class='red_bold'>Important:</span>Lorem ipsum dwdwdw</td>
            </tr>
            <tr>
                <td><b>ICTO</b></td>
            </tr>
            </body>
        </table>
        """


    if len(df.index) != 0:
        html2 =+ f"""
            <div id='policy_info'></div>

            <div class='table_container'>
            <form method='POST'>
            <table class='table' cellspacing='0' cellpadding='0'>
                <thead>
                <tr>
        """

        # return names of columns
        headers = {
            "SSID": 'Subsystem',
            "DBNAME": 'Database',
            "TSNAME": 'Tablespace',
            "SAVE_PROFIL": 'Backup',
            "POLICY_OK": "Attest"
        }

        for i in df:
            for x, y in headers.items():
                if x == i:
                    if i == "POLICY_OK":
                        print('test')

        html2 += f"</tr><thead><tbody>"

        for i, row in df.iterrows():
            html2 += "<tr>"
            html2 += f"<td>{row.SSID}</td>"
            html2 += f"<td>{row.DBNAME}</td>"
            html2 += f"<td>{row.TSNAME}</td>"
            html2 += f"<td><textarea id='feedback_{i}' name='feedback{i}' rows='2' cols='50'></textarea>"

            if row.POLICY_OK == "Confirmed":
                html2 += f"""
                    <td>
                    <input type='radio' id='policy_ok{i}' name='backup' value='Confirmed' checked='checked'>
                    <label class='green' for='policy_ok{i}'>All good</label>
                    <br />
                    <input type='radio' id='policy_not_ok{i}' name='backup' value=''>
                    <label class='green' for='policy_not_ok{i}'>Not good</label>
                    </td>
                """

            else:
                html2 += f"""
                    <td>
                    <input type='radio' id='policy_ok{i}' name='backup' value='Confirmed'>
                    <label class='green' for='policy_ok{i}'>All good</label>
                    <br />
                    <input type='radio' id='policy_not_ok{i}' name='backup' value='' checked='checked'>
                    <label class='green' for='policy_not_ok{i}'>Not good</label>
                    </td>
                """

        html2 += "</tr></tbody>"
        html2 += "</table>"
        html2 += "<button id='submit' type='submit'>Attest</button></form></div></div></div></div></body>"

    else:
        html2 += "test"

    return html2

@app.route('/', methods=['POST', 'GET'])
def save():
    remoteuser = get_PID()

    if request.method == 'POST':
        my_db2 = mf.mf
        dictionary = request.form.to_dict()

        if len(dictionary) % 5 == 0:
            records = int(len(dictionary) / 5)
        else:
            raise Exception("Number of parameter is not valid")
        
        for i in range(records):
            if dictionary['DBNAME'+str(i)].strip() == 'xxx':
                dictionary['DBNAME'+str(i)] = 'xx2'

            sqlUpdate = f"""
                UPDATE SAVEPROFILE
                SET .....
                WHERE .....
            """

            cursor = my_db2.conn.cursor()
            cursor.execute(sqlUpdate)
            my_db2.conn.commit()
        
        my_db2 = None
        return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
