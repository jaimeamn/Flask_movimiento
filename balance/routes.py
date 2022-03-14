from flask import render_template, request, redirect, url_for, flash
from balance import app
from datetime import date

import csv

MOVIMIENTOS_FILE = "data/movimientos.csv"

@app.route("/")
def inicio():
    lista_movimientos = []
    fichero_mv = open(MOVIMIENTOS_FILE, "r")

    #----------------------------------------------------
    cab = fichero_mv.readline()
    linea = fichero_mv.readline()
    while linea != "":
        campos = linea.split(",")
        lista_movimientos.append(
            {
                "fecha": campos[0],
                "hora": campos[1],
                "concepto": campos[2],
                "es_ingreso": True if campos[3] == '1' else False,
                "cantidad": float(campos[4])
            }
        )

        linea = fichero_mv.readline()


    linea = fichero_mv.readline()

    fichero_mv.close()
    return render_template("lista_movimientos.html", 
                            movimientos = lista_movimientos)

@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("nuevo_movimiento.html", datos={})
    else:
        # recuperar los campos del request.form
        nombres_campo = ['fecha', 'hora', 'concepto', 'es_ingreso', 'cantidad']

        """
         validar la entrada
            - No fechas/horas futuras 
            - Fecha requerida
            - Fecha formato y valor correcto
            - Hora requerida
            - Hora formato y valor correcto
            - Concepto es requerido
            - Concepto max 100 car
            - es_ingreso: on / off
            - cantidad número mayor que cero
        """
        formulario = dict(request.form)
        formulario.pop('aceptar')

        cantidad = formulario['cantidad']
        fecha = formulario['fecha']

        try:
            cantidad = float(cantidad)
            if cantidad <= 0:
                flash("La cantidad debe ser positiva.")
                todo_bien = False
        except ValueError:
            flash("La cantidad debe ser numérica.")
            todo_bien = False        

        try:
            fecha = date.fromisoformat(fecha)
            if fecha > date.today():
                flash("La fecha no puede ser posterior a hoy.")
                todo_bien = False
        except ValueError as e:
            flash(f"Fecha incorrecta: {e}")
            todo_bien = False

        if not todo_bien:
            return render_template("nuevo_movimiento.html", datos = formulario)

        # grabar el nuevo registro en movimientos.csv
        fichero_mv = open(MOVIMIENTOS_FILE, 'a')
        writer = csv.DictWriter(fichero_mv, fieldnames=nombres_campo)
        d = dict(request.form)
        d.pop('aceptar')
        writer.writerow(d)
        fichero_mv.close()

        return redirect(url_for("inicio"))