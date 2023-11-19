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
    remoteuser = get_PID()

    sql = "SELECT * FROM SAVEPROFILE WHERE DB_OWNER_PID = ?"
    params = {remoteuser}

    sqlSelection = "SELECT DB_OWNER_NAME, DB_OWNER_PID FROM SAVEPROFILE WHERE DB_OWNER_PID = '{remoteuser}' LIMIT 1"

    try:
        my_db2 = mf.mf
        df = my_db2.Db2_runsql(sql, params)
        dfSelection = my_db2.Db2_runsql(sql)
        my_db2 = None
    except:
        if sys.platform == "zos":
            print('exception')

    icunique = df['cto'].unique()

    # return names of columns
    headers = {
        "SSID": 'Subsystem',
        "DBNAME": 'Database',
        "TSNAME": 'Tablespace',
        "SAVE_PROFIL": 'Backup',
        "POLICY_OK": "Attest"
    }

    return render_template('review.html', remoteuser=remoteuser, df=df, icunique=icunique, headers=headers)

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
