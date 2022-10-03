from src.data.search import *
from flask import Flask, url_for, redirect, jsonify, request

app = Flask(__name__)

@app.route("/")
def pengalihan():
    return redirect(url_for("searchKomik"))

@app.route("/api/komik/",methods=["POST","GET"])
def searchKomik():
    if request.method=="GET":
        key = request.args.get("judul")
        if(key):
            req = Main.request("https://data.komiku.id/cari/?post_type=manga&s="+key)
            if(req['hasil-pencarian']!=0):
                return jsonify(req)
            else:
                return jsonify(
                    {
                        "error":"hasil pencarian tidak ditemukan"
                    }
                )
        else:
            return jsonify(
                {
                    "error":"judul non harap input judul! contoh: /api/komik/?judul=immortal+king '+' pengganti spasi"
                }
            )
    else:
        return jsonify(
            {
                "error":"harap gunakan method GET"
            }
        )

if __name__=="__main__":
    app.run(debug=True)
