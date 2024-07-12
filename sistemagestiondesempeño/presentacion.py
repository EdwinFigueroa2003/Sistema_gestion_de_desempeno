from flask import Blueprint,render_template,session,redirect,url_for

presentacion=Blueprint("presentacion",__name__,static_folder="static",template_folder="templates")

@presentacion.route("/presentacion",methods = ['GET', 'POST'])
@presentacion.route("/")
def vista_presentacion():
    #código de validación de control de acceso al menú
    return redirect('/inicio') 