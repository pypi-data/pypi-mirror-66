from random import randint, uniform,random
from sympy import *
from sympy.plotting import plot,plot3d
import pandas as pd
import numpy as np
import re
from IPython.core.display import HTML, display
from ipywidgets import interact, interact_manual,interactive, widgets
import yagmail
import matplotlib.pyplot as plt


cien="Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar" \
    " aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de 20 casas de barro " \
     "y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, " \
     "blancas y enormes como huevos prehistóricos." \
     " El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo."
cien=cien.split()
cien=[int(len(i))%3 for  i in cien]
x,y,z,l=symbols("x,y,z,l")
init_printing(use_latex=True )

def generador(n):
    N=np.sin(3*n+2)-500*np.sin(n)
    M=np.sin(5*n+1)-500*np.cos(n)
    K=np.sin(3*n+2)-500*np.cos(n)**2
    values=[N,M,K]
    ST=""

    for i in cien:
        ST=ST+(i+1)*re.sub(r"[^1-9]","",str(values[i]))
    ST=np.array([int(i) for i in list(ST)])
    return ST[:500]

def Examen2MCG2(n):
    Xa,Xb,Pa,Pb =symbols("Xa,Xb,Pa,Pb")
    K,L =symbols("K,L")

    GEN=generador(n)
    ex1=GEN[10]%5+1
    ex2=GEN[15]%5+1
    ex3=GEN[20]%3
    ey1=GEN[30]%5+1
    ey2=GEN[40]%5+1
    c1=-GEN[45]%8-1
    c2=GEN[45]+GEN[20]%6-11
    c3=GEN[15]-6+GEN[35]%2
    c4=GEN[21]%7+2
    
    
    A=(GEN[45]%4+2)*0.5
    B=(GEN[55]%4+1)*0.5
    C=GEN[65]+int(np.floor(4*A*B))+2
    AA=GEN[32]+1
    BB=GEN[97]+1
    CC=(GEN[26]*10+GEN[12])*5+100
    
    ma=(GEN[45]*10+GEN[32]+1)*50
    ba=200*ma*(GEN[15]*10+GEN[28]+1)
    
    mb=(GEN[85]*10+GEN[82]+1)*50
    bb=200*ma*(GEN[35]*10+GEN[38]+1)
    
    e1=Eq(Pa,ba-ma*Xa)
    e2=Eq(Pb,bb-mb*Xb)
   
    
    F=c2*x**ex2*y**ey1+c1*x**ex3*y**ey2
    G=c3*((ex3%2+1)*x-(ex3%2)*y)*E**(x**(ex2%2+1)+y**(ex2%2+2))
    T=A*L**2+B*K**2-C*K*L-AA*K-BB*L+CC
    
    a=((GEN[22]+GEN[14]+GEN[11]%5+10)**2)*3
    b=(GEN[22]+GEN[14]+GEN[11]%3+3)
    f=b*x*y*z
    r=2*x*z+2*y*z+x*y-a
    R=Eq(r+a,a)
    
    sexa=(GEN[19]%9+1)*0.1
    sexm=(GEN[35]%8+2)*2000
    sexn=(GEN[100]%8+2)*2000 
    sexpre=sexm*sexn
    sexP=x**sexa*y**(1-sexa)

    res={}
    RES={"R1":"","R2":""}
    
    def Ejercicio1():
        def resa(d):
            try:
                d=sympify(d)
                plot3d(d)
                res["dx"]=[str(d)]
            except:
                pass
            return d
        def resb(d):
            try:
                d=sympify(d)
                plot3d(d)
                res["dy"]=[str(d)]
            except:
                pass
            return d
        display(HTML("<h3>Primer ejercicio: </h3> <p>Calcule las derivadas parciales de primer orden de la "
                         "función $f(x)="+str(latex(F))+".$ Responda usando el lenguaje de Sympy para Python, "
                        "es decir, si la respuesta es $x^2$, escriba: <i>x**2</i>.</p><p></p><p></p>"))

        def itemA():
            display(HTML("<p>$(a).$ Ingrese la derivada de $f(x)="+str(latex(F))+"$ respecto a $x$:</p><p></p><p></p>"))
            d1=interactive(resa,d=widgets.Text(
                value='x**2',
                description='$\partial f/\partial x = $ '
            ))  
            display(d1)
            return 

        def itemB():
            display(HTML("<p> $(b).$Ingrese la derivada de $f(x)="+str(latex(F))+"$ respecto a $y$:</p><p></p><p></p>"))
            d2=interactive(resb,d=widgets.Text(
                value='x**2',
                description='$\partial f/\partial x = $ '
            ))
            display(d2)
            return d2.result
        a=itemA()
        b=itemB()
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p1= open("p1.png", "wb")
                p1.write(upload_file[img_name]["content"])
                p1.close()
                ra=latex(sympify(res["dx"][0]))
                rb=latex(sympify(res["dy"][0]))
                R1="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el primer ejercicio son:</h3>"+"<p>$\cfrac{\partial f}{\partial x} ="+ra+" $</p><p>$\cfrac{\partial f}{\partial y} ="+rb+" $</p></div>"
                display(HTML(R1))
                RES["R1"]=R1
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))



        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.py,.ipynb',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)


        return


  
    
    def Ejercicio2():
        def resc(d):
            try:
                d=sympify(d)
                plot3d(d)
                res["dx1"]=[str(d)]
            except:
                pass
            return d
        def resd(d):
            try:
                d=sympify(d)
                plot3d(d)
                res["dy1"]=[str(d)]
            except:
                pass
            return d
        display(HTML("<h3>Segundo ejercicio: </h3> <p>Calcule las derivadas parciales de primer orden de la "
                         "función $g(x)="+str(latex(G))+".$ Responda usando el lenguaje de Sympy para Python, "
                        "es decir, si la respuesta es $x^2$, escriba: <i>x**2</i>.</p><p></p><p></p>"))

        def itemC():
            display(HTML("<p>$(a).$ Ingrese la derivada de $g(x)="+str(latex(G))+"$ respecto a $x$:</p><p></p><p></p>"))
            d1=interactive(resc,d=widgets.Text(
                value='x**2',
                description='$\partial f/\partial x = $ '
            ))  
            display(d1)
            return 

        def itemD():
            display(HTML("<p>$(b).$ Ingrese la derivada de $g(x)="+str(latex(G))+"$ respecto a $y$:</p><p></p><p></p>"))
            d2=interactive(resd,d=widgets.Text(
                value='x**2',
                description='$\partial f/\partial x = $ '
            ))
            display(d2)
            return d2.result
        a=itemC()
        b=itemD()
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p2= open("p2.png", "wb")
                p2.write(upload_file[img_name]["content"])
                p2.close()
                ra=latex(sympify(res["dx1"][0]))
                rb=latex(sympify(res["dy1"][0]))
                R2="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el segundo ejercicio son:</h3>"+ "<p>$\cfrac{\partial g}{\partial x} ="+ra+" $</p><p>$\cfrac{\partial g}{\partial y} ="+rb+" $</p></div>"
                display(HTML(R2))
                RES["R2"]=R2        
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))



        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.py,.ipynb',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)
        return
    
    
    def Ejercicio3():

        def dem1():
            p=plot(ba-ma*Xa,(Xa,-5,ba/ma+5))
            return p
        def dem2():
            p=plot(bb-mb*Xb,(Xb,-5,bb/mb+5))
            return p
        def rese(d):
            d=sympify(d)
            res["Xa"]=[str(d)]
            return 
        def resf(d):
            d=sympify(d)
            res["Xb"]=[str(d)]
            return


        display(HTML("<h3>Tercer ejercicio: </h3> <p>La empresa en la que usted trabaja desea conocer los niveles de producción que harán que la venta de $Xa$ unidades del producto A y $Xb$ unidades del producto B generen los ingresos más altos posibles, sabiendo que las demandas de cada uno de los modelos vienen dadas por:</p><p></p><p></p> <ul>   <li>Demanda del producto A es:$"+str(latex(e1))+"$ </li></ul> "))

        d5=interactive(dem1)

        display(d5)
        
        display(HTML("<ul>   <li>Demanda del producto B es:$"+str(latex(e2))+"$ </li></ul> "))

        d6=interactive(dem2)

        display(d6)
        
        display(HTML("<p> Determine dichos niveles de producción.</p> "))
        
        
        def itemE():
            display(HTML("<p>$(a).$ Ingrese la cantidad de productos A:</p><p></p><p></p>"))
            d1=interactive(rese,d=widgets.FloatText(
                value=0,
                description='$Xa = $ '
            ))  
            display(d1)
            return 

        def itemF():
            display(HTML("<p>$(b).$ Ingrese la cantidad de productos B:</p><p></p><p></p>"))
            d1=interactive(resf,d=widgets.FloatText(
                value=0,
                description='$Xb = $ '
            ))  
            display(d1)
            return 
        a=itemE()
        b=itemF()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p3= open("p3.png", "wb")
                p3.write(upload_file[img_name]["content"])
                p3.close()
                ra=latex(sympify(res["Xa"][0]))
                rb=latex(sympify(res["Xb"][0]))
                R3="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el tercer ejercicio son:</h3>"+ "<p>$Xa ="+ra+" $</p><p>$Xb ="+rb+" $</p></div>"
                display(HTML(R3))
                RES["R3"]=R3        
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            
                        
                        
                                           
        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.ipynb,.py',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)
        return

    
    
    def Ejercicio4():

        def dem1():
            p=plot3d(T)
            return p
        def resg(d):
            d=sympify(d)
            res["K"]=[str(d)]
            return 
        def resh(d):
            d=sympify(d)
            res["L"]=[str(d)]
            return


        display(HTML("<h3>Cuarto ejercicio: </h3> <p>Empleando L unidades del insumo de mano del obra y K unidades de capital una empresa fabrica cierta cantidad de unidades de su artículo. Si el costo total $T$, en millones de pesos, viene dado por:</p><p></p><p></p> <p>$ T ="+str(latex(T))+"$ </p> "))

        d7=interactive(dem1)

        display(d7)
        
           
        display(HTML("<p> Determine la cantidad de unidades de cada insumo que hacen que $T$ sea mínimo.</p> "))
        
        
        def itemG():
            display(HTML("<p>$(a).$ Ingrese la cantidad $K$:</p><p></p><p></p>"))
            d1=interactive(resg,d=widgets.FloatText(
                value=0,
                description='$K = $ '
            ))  
            display(d1)
            return 

        def itemH():
            display(HTML("<p>$(b).$ Ingrese la cantidad $L$:</p><p></p><p></p>"))
            d1=interactive(resh,d=widgets.FloatText(
                value=0,
                description='$L = $ '
            ))  
            display(d1)
            return 
        a=itemG()
        b=itemH()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p4= open("p4.png", "wb")
                p4.write(upload_file[img_name]["content"])
                p4.close()
                ra=latex(sympify(res["K"][0]))
                rb=latex(sympify(res["L"][0]))
                R4="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el cuarto ejercicio son:</h3>"+ "<p>$K ="+ra+" $</p><p>$L ="+rb+" $</p></div>"
                display(HTML(R4))
                RES["R4"]=R4        
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            
                        
                        
                                           
        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.py,.ipynb',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)
        return
    
    def Ejercicio5():

        def resi(d):
            d=sympify(d)
            res["mx"]=[str(d)]
            return 
        def resj(d):
            d=sympify(d)
            res["my"]=[str(d)]
            return
        def resk(d):
            d=sympify(d)
            res["mz"]=[str(d)]
            return
        
        def resl(d):
            d=sympify(d)
            res["Mx"]=[str(d)]
            return 
        def resm(d):
            d=sympify(d)
            res["My"]=[str(d)]
            return
        def resn(d):
            d=sympify(d)
            res["Mz"]=[str(d)]
            return


        display(HTML("<h3>Quinto ejercicio: </h3> <p>Encuentre los valores máximos y mínimos de la función $f(x,y,z) = "+str(latex(f))+" $ sujeta a la restricción: "+str(latex(R)) +" </p><p></p><p></p>"))
        
        
        def itemIJK():
            display(HTML("<p>$(a).$ Ingrese el mínimo de la función:</p><p></p><p></p>"))
            d1=interactive(resi,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            
            d2=interactive(resj,d=widgets.FloatText(
                value=0,
                description='$y = $ '
            ))
                
            d3=interactive(resk,d=widgets.FloatText(
                value=0,
                description='$z = $ '
            ))
            H=widgets.HBox([d1,d2,d3])
            display(H)
            return 

        def itemLMN():
            display(HTML("<p>$(a).$ Ingrese el máximo de la función:</p><p></p><p></p>"))
            d1=interactive(resl,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            
            d2=interactive(resm,d=widgets.FloatText(
                value=0,
                description='$y = $ '
            ))
                
            d3=interactive(resn,d=widgets.FloatText(
                value=0,
                description='$z = $ '
            ))
            H=widgets.HBox([d1,d2,d3])
            display(H)
            return 
        a=itemIJK()
        b=itemLMN()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p5= open("p5.png", "wb")
                p5.write(upload_file[img_name]["content"])
                p5.close()
                ra=latex(sympify([res["mx"][0],res["my"][0],res["mz"][0]]))
                rb=latex(sympify([res["Mx"][0],res["My"][0],res["Mz"][0]]))
                R5="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el quinto ejercicio son:</h3>"+ "<p>$Min ="+ra+" $</p><p>$Max ="+rb+" $</p></div>"
                display(HTML(R5))
                RES["R5"]=R5        
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            
                        
                        
                                           
        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.py,.ipynb',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)
        return
    
    def Ejercicio6():

        def reso(d):
            d=sympify(d)
            res["MO"]=[str(d)]
            return 
        def resp(d):
            d=sympify(d)
            res["KA"]=[str(d)]
            return

        display(HTML("<h3>Sexto ejercicio: </h3> <p>La función de producción de una empresa es $P(x,y) = "+str(latex(sexP))+" $ en donde $x$ y $y$ representan el número de unidades de mano de obra y de capital utilizadas y $P$ es el número de unidades elaboradas del producto. Cada unidad de mano de obra tiene un costo de  " +str(sexm)+ " y cada unidad de capital cuesta  " +str(sexn)+ "  y la empresa dispone de  " +str(sexpre)+ "  destinados a producción. Determine el número de unidades de mano de obra y de capital que la empresa debe emplear para obtener producción máxima.</p><p></p><p></p>"))
        
        
        
        def itemO():
            display(HTML("<p>$(a).$ Ingrese el número de unidades de mano de obra:</p><p></p><p></p>"))
            d1=interactive(reso,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            
            display(d1)
            return 

        def itemP():
            display(HTML("<p>$(a).$ Ingrese el capital:</p><p></p><p></p>"))
            d1=interactive(resp,d=widgets.FloatText(
                value=0,
                description='$y = $ '
            ))  
            
           
            display(d1)
            return 
        a=itemO()
        b=itemP()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                p6= open("p6.png", "wb")
                p6.write(upload_file[img_name]["content"])
                p6.close()
                ra=latex(sympify(res["MO"][0]))
                rb=latex(sympify(res["KA"][0]))
                R6="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el sexto ejercicio son:</h3>"+ "<p>$Mano_de_obra ="+ra+" $</p><p>$Capital ="+rb+" $</p></div>"
                display(HTML(R6))
                RES["R6"]=R6                
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            
                        
                        
                                           
        B=widgets.Button(
            description='Guardame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Guardar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        B.on_click(guardar)   

        Upload=widgets.FileUpload(
            description="Soporte Respuesta",
            accept='image/*,.py,.ipynb',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False  # True to accept multiple files upload else False
        )

        display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)
        return
    
    def enviar():
        info={}
        def correoprofe(d):    
            info["Correo del Profesor"]=d
            return prof
        def nombre(d):
            info["Nombre del alumno"]=d
            return nom

        prof=widgets.Text(description="Correo Profesor:")
        nom=widgets.Text(description="Nombre Completo:")

        def boton_enviar(B):  
            try:
                message="""<html><head></head><body><p>El alumno con identificación"""+str(n)+""" envía lo siguiente:</p> """+RES["R1"]+RES["R2"]+RES["R3"]+RES["R4"]+RES["R5"]+RES["R6"]+"""</body></html>"""
                message=bytes(message,"utf-8")
                f = open('Respuestas'+info["Nombre del alumno"]+'.html','wb')
                f.write(message)
                f.close()
                display(message)
                receiver = info["Correo del Profesor"]
                body = "El alumno "+info["Nombre del alumno"]+ " le envía la siguiente prueba"
                filename = 'Respuestas'+info["Nombre del alumno"]+'.html'
                yag = yagmail.SMTP("avamatext@gmail.com", 'Extern@do123')
                yagmail.register('avamatext', 'Extern@do123')
                yag.send(
                    to=receiver,
                    subject=info["Nombre del alumno"]+"Respuestas",
                    contents=body, 
                    attachments=[filename,"p1.png","p2.png","p3.png","p4.png","p5.png","p6.png","prueba.csv"],
                )
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No guardaste todas tus respuestas, verifica!</h3>"))


        style = {'description_width': 'initial'}


        d1=interactive(correoprofe,d=widgets.Text(description="Correo Profesor:",style=style))
        d2=interactive(nombre,d=widgets.Text(description="Nombre Completo:",style=style))
        B=widgets.Button(
            description='Envíame aquí',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Enviar Respuesta',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        display(d1)
        display(d2)
        B.on_click(boton_enviar)
        display(B)


    E1=interactive(Ejercicio1)
    E2=interactive(Ejercicio2)
    E3=interactive(Ejercicio3)
    E4=interactive(Ejercicio4)
    E5=interactive(Ejercicio5)
    E6=interactive(Ejercicio6)
    ENV=interactive(enviar)
    accordion = widgets.Accordion(children=[E1,E2,E3,E4,E5,E6,ENV])

    acc=["Ejercicio 1", "Ejercicio 2","Ejercicio 3","Ejercicio 4","Ejercicio 5","Ejercicio 6","Enviar"]
    for i in range(len(acc)):
        accordion.set_title(i,acc[i])
    display(accordion)
