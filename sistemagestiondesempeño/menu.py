from flask import Blueprint,render_template,session,redirect,url_for

menu=Blueprint("menu",__name__,static_folder="static",template_folder="templates")

@menu.route("/menu",methods = ['GET', 'POST'])
@menu.route("/")
def vista_menu():
    #código de validación de control de acceso al menú
    return redirect('/inicio') 