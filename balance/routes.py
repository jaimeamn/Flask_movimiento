from flask import render_template
from balance import app

@app.route("/")
def inicio():
    lista_movimiento =[
        {
            "fecha": "2022-01-06",
            "hora": "13:23:34",
            "concepto": "reyes",
            "es_ingreso": False,
            "cantidad": 100
        },
        {
            "fecha": "2022-01-06",
            "hora": "13:23:34",
            "concepto": "jajajaj",
            "es_ingreso": True,
            "cantidad": 666
        },

        {
            "fecha": "2022-01-06",
            "hora": "13:23:34",
            "concepto": "jajajaj",
            "es_ingreso": True,
            "cantidad": 666
        },
        {
            "fecha": "2022-01-06",
            "hora": "13:23:34",
            "concepto": "jkakaka",
            "es_ingreso": False,
            "cantidad": 180
        }
    ]
    return render_template("lista_movimientos.html", movimiento = lista_movimiento)