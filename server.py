from flask import Flask, request
import sqlite3
import json


app = Flask(__name__)


#Schema of db
#could add a user column but for the scope of this project not need

#Schema of email
#mail = (id uuid, recipient String, sender String, message String, archieved Boolean)


#curl --header "Content-Type: application/json" --request POST --data "{"""id""":"""aa6c44e9-e340-4263-b931-072637480197"""
#,"""sender""":"""you""","""message""":"""adasdsasdas"""}" http://127.0.0.1:5000/email/me

class Mail:
    def __init__(self, id, sender, message, archived):
        self.id = id
        self.sender = sender
        self.message = message
        self.archived = archived



@app.route("/email/<address>", methods = ['POST','GET'])
def email(address):
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    #if user is found
    if request.method=='POST':
        #expect the format of the post request json to be
        #   {id: UUID
        #    sender: String
        #    message: String
        #   }
        package = request.get_json()
        cursor.execute("INSERT INTO mail VALUES ('{}', '{}','{}', '{}', 0);".format(package['id'], address,package['sender'],package['message']))
        conn.commit()
        #return 200 after saved
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    elif request.method=='GET':
        #Obviously going to need some authentication here
        #but ignored for now
        cursor.execute("SELECT * FROM mail WHERE recipient='{}';".format(address))
        conn.commit()

        mail_list = cursor.fetchall()
        result = []
        for mail in mail_list:
            temp = Mail(mail[0],mail[2],mail[3], mail[4])
            result.append(temp.__dict__)
        return json.dumps(result), 200, {'ContentType': 'application/json'}


@app.route("/email/<address>/sent", methods = ['GET'])
#misread instructions, not needed, kept for testing sake
def sent_mail(address):
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    # user will be None if cannot find such user
    cursor.execute("SELECT * FROM mail WHERE sender = '{}';".format(address))
    conn.commit()

    mail_list = cursor.fetchall()

    return json.dumps(mail_list), 200, {'ContentType': 'application/json'}

@app.route("/email/mail/<mail_id>", methods = ['PUT','DELETE'])
def archive_email(mail_id):
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    if request.method=='DELETE':
        cursor.execute("DELETE FROM mail WHERE id = '{}'".format(mail_id))
        conn.commit()
    elif request.method=='PUT':
        package = request.get_json()
        if package['archived']==0:
            cursor.execute("UPDATE mail SET archived = 0 WHERE id='{}';".format(mail_id))
        else:
            cursor.execute("UPDATE mail SET archived = 1 WHERE id='{}';".format(mail_id))
        conn.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__=="__main__":
    app.run(debug=True)
