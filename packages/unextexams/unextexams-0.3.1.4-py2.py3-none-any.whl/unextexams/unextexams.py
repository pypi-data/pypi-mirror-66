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
ppp,x,y,z,l=symbols("p,x,y,z,l")
init_printing(use_latex=True )
style = {'description_width': 'initial'}

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
    C=int(np.floor(sqrt(4*A*B)))-0.2*GEN[12]
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
    G=c3*((ex3%2+1)*x-(ex3%2)*y)*E**(x**(ex2%2+1)+y**(ex2%2+GEN[22]*0.15))
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

    res={"n":n}
    RES={"R1":"","R2":""}
    archivos={}
    
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
                description='$\partial f/\partial y = $ '
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
                nombrearchivo1="p1"+img_name
                p1= open(nombrearchivo1, "wb")
                p1.write(upload_file[img_name]["content"])
                p1.close()
                ra=latex(sympify(res["dx"][0]))
                rb=latex(sympify(res["dy"][0]))
                R1="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el primer ejercicio son:</h3>"+"<p>$\cfrac{\partial f}{\partial x} ="+ra+" $</p><p>$\cfrac{\partial f}{\partial y} ="+rb+" $</p></div>"
                display(HTML(R1))
                RES["R1"]=R1
                archivos["1"]=nombrearchivo1
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
                description='$\partial f/\partial y = $ '
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
                nombrearchivo2="p2"+img_name
                p2= open(nombrearchivo2, "wb")
                p2.write(upload_file[img_name]["content"])
                p2.close()
                ra=latex(sympify(res["dx1"][0]))
                rb=latex(sympify(res["dy1"][0]))
                R2="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el segundo ejercicio son:</h3>"+ "<p>$\cfrac{\partial g}{\partial x} ="+ra+" $</p><p>$\cfrac{\partial g}{\partial y} ="+rb+" $</p></div>"
                display(HTML(R2))
                RES["R2"]=R2   
                archivos["2"]=nombrearchivo2
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
                nombrearchivo3="p3"+img_name
                p3= open(nombrearchivo3, "wb")
                p3.write(upload_file[img_name]["content"])
                p3.close()
                ra=latex(sympify(res["Xa"][0]))
                rb=latex(sympify(res["Xb"][0]))
                R3="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el tercer ejercicio son:</h3>"+ "<p>$Xa ="+ra+" $</p><p>$Xb ="+rb+" $</p></div>"
                display(HTML(R3))
                RES["R3"]=R3  
                archivos["3"]=nombrearchivo3
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
                nombrearchivo4="p4"+img_name
                p4= open(nombrearchivo4, "wb")
                p4.write(upload_file[img_name]["content"])
                p4.close()
                ra=latex(sympify(res["K"][0]))
                rb=latex(sympify(res["L"][0]))
                R4="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el cuarto ejercicio son:</h3>"+ "<p>$K ="+ra+" $</p><p>$L ="+rb+" $</p></div>"
                display(HTML(R4))
                RES["R4"]=R4   
                archivos["4"]=nombrearchivo4
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
                nombrearchivo5="p5"+img_name
                p5= open(nombrearchivo5, "wb")
                p5.write(upload_file[img_name]["content"])
                p5.close()
                ra=latex(sympify([res["mx"][0],res["my"][0],res["mz"][0]]))
                rb=latex(sympify([res["Mx"][0],res["My"][0],res["Mz"][0]]))
                R5="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el quinto ejercicio son:</h3>"+ "<p>$Min ="+ra+" $</p><p>$Max ="+rb+" $</p></div>"
                display(HTML(R5))
                RES["R5"]=R5    
                archivos["5"]=nombrearchivo5
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
                nombrearchivo6="p6"+img_name
                p6= open(nombrearchivo6, "wb")
                p6.write(upload_file[img_name]["content"])
                p6.close()
                ra=latex(sympify(res["MO"][0]))
                rb=latex(sympify(res["KA"][0]))
                R6="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el sexto ejercicio son:</h3>"+ "<p>$Mano_de_obra ="+ra+" $</p><p>$Capital ="+rb+" $</p></div>"
                display(HTML(R6))
                RES["R6"]=R6   
                archivos["6"]=nombrearchivo6
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
                    attachments=[filename,archivos["1"],archivos["2"],archivos["3"],archivos["4"],archivos["5"],archivos["6"],"prueba.csv"],
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
    
    return






def Examen2MCG1(n):
    GEN=generador(n)
    
    a1=GEN[19]%4+1
    c1=GEN[12]-GEN[15]
    b1=np.floor(np.sqrt(np.abs(4*a1*c1)))+2
    
    
    a2=GEN[23]%4+1
    c2=GEN[14]
    b2=np.floor(np.sqrt(np.abs(4*a2*c2)))
    
    
    a3=GEN[15]%4+1
    c3=GEN[16]
    b3=np.floor(np.sqrt(np.abs(4*a3*c3)))-GEN[21]
    
    
    Ec1=Eq(expand((2*x-a1)*(x-a2)),expand((x-a3)*(x-a2)))
    Ec2=Eq(2*factor((x-a1)*(x-c3)),factor((x-c2)*(x-a2)))
    Ec3=Eq((5*x-5*a1)*(x-c3),factor((x-c1)*(x-c2)))
    
    aa=((GEN[32]+GEN[15]+3*GEN[18]+2*GEN[14])%15+30)*100
    bb=GEN[32]*10+10
    xx=(GEN[21]+9*GEN[14])%20+10
    
    numhab=GEN[24]+10*GEN[34]+200
    renta=((5*GEN[44]+10*GEN[54])%70+10)*10
    aumento=(GEN[22]+GEN[32]+20)
    habvac=(GEN[45]+GEN[12])%18+2
    numeroaumentos=GEN[13]%6+3
    ingresos=(numhab-habvac*numeroaumentos)*(renta+aumento*numeroaumentos)
    
    personas=(GEN[32]*9+GEN[17]*5+GEN[43]*7)%130+120
    precio=((GEN[11]*8+GEN[12]*9+GEN[18]*52+GEN[44]*7)%750+150)*1000
    preciosillavacia=((GEN[21]*8+GEN[22]*11+GEN[18]*5+GEN[22]*7)%40+10)*1000
    sillavacia=((GEN[11]*8+GEN[12]*91+GEN[18]*5+GEN[42]*7)%30+10)
    ingresosav=(precio+preciosillavacia*sillavacia)*(personas-sillavacia)



    res={}
    RES={"R1":"","R2":""}
    archivos={}
    
    def Ejercicio1():          
        def resa1(d):
            try:
                res["p1"]=str(d)                
            except:
                pass
            return d
        
        
        def resa2(d,e):
            try:
                res["p1"]=str([d,e])
            except:
                pass
            return d
        def resb1(d):
            try:
                res["p2"]=str(d)                
            except:
                pass
            return d
        
        
        def resb2(d,e):
            try:
                res["p2"]=str([d,e])
            except:
                pass
            return d
        def resc1(d):
            try:
                res["p3"]=str(d)                
            except:
                pass
            return d
        
        
        def resc2(d,e):
            try:
                res["p3"]=str([d,e])
            except:
                pass
            return d
        
        def cantidaddesoluciones1(cant):
            if cant == "No hay solución":
                res["p1"]="NOSOL"
            elif cant == "Una solución":
                d1=interactive(resa1,d=widgets.IntText(description="Solución:"))
                display(d1)
            else:
                d1=interactive(resa2,d=widgets.IntText(description="Solución 1: "),e=widgets.IntText(description="Solución 2: "))
                display(d1)
            return
        
        def cantidaddesoluciones2(cant):
            if cant == "No hay solución":
                res["p2"]="NOSOL"
            elif cant == "Una solución":
                d1=interactive(resb1,d=widgets.IntText(description="Solución:"))
                display(d1)
            else:
                d1=interactive(resb2,d=widgets.IntText(description="Solución 1: "),e=widgets.IntText(description="Solución 2: "))
                display(d1)
            return
        
        def cantidaddesoluciones3(cant):
            if cant == "No hay solución":
                res["p3"]="NOSOL"
            elif cant == "Una solución":
                d1=interactive(resc1,d=widgets.IntText(description="Solución:"))
                display(d1)
            else:
                d1=interactive(resc2,d=widgets.IntText(description="Solución 1: "),e=widgets.IntText(description="Solución 2: "))
                display(d1)
            return
        
        
        display(HTML("<h3>Primer ejercicio: </h3> <p>Determine la solución de las siguientes ecuaciones:</p>"
                     "<p>Recuerde responder usando el lenguaje de Sympy para Python, "
                        "es decir, si la respuesta es $x^2$, escriba: <i>x**2</i>.</p><p></p><p></p>"))

        def itemA():
            display(HTML("<p>$(a).$ Ecuación 1: $"+str(latex(Ec1))+".$</p><p></p><p></p>"))
            d1=interactive(cantidaddesoluciones1,cant=widgets.Dropdown(
                style=style,
                options=["No hay solución","Una solución","Dos soluciones"],
                description='Cantidad de soluciones '
            ))  
            display(d1)
            return 

        def itemB():
            display(HTML("<p>$(b).$ Ecuación 2: $"+str(latex(Ec2))+".$</p><p></p><p></p>"))
            d1=interactive(cantidaddesoluciones2,cant=widgets.Dropdown(
                style=style,
                options=["No hay solución","Una solución","Dos soluciones"],
                description='Cantidad de soluciones '
            ))  
            display(d1)
            return
        
        def itemC():
            display(HTML("<p>$(c).$ Ecuación 3: $"+str(latex(Ec3))+".$</p><p></p><p></p>"))
            d1=interactive(cantidaddesoluciones3,cant=widgets.Dropdown(
                style=style,
                options=["No hay solución","Una solución","Dos soluciones"],
                description='Cantidad de soluciones '
            ))  
            display(d1)
            return 
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv") 
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                nombrearchivo1="p1"+img_name
                p1= open(nombrearchivo1, "wb")
                p1.write(upload_file[img_name]["content"])
                p1.close()
                ra=res["p1"]
                rb=res["p2"]
                rc=res["p3"]
                R1="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el primer ejercicio son:</h3><p>Ecuación1:  "+ra+"</p><p>Ecuación 2: "+rb+" </p><p>Ecuación3:  "+rc+"</p></div>"
                display(HTML(R1))
                RES["R1"]=R1
                archivos["1"]=nombrearchivo1
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            return
        
        
        a=itemA()
        b=itemB()
        c=itemC()



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

        display(HTML("<p>Ingrese aquí un soporte del ejercicio (puede ser imagen o cuaderno de python):</p>"))
        display(Upload)
        display(HTML("<p>Guarde sus respuestas</p>"))
        display(B)


        return
    
    def Ejercicio2():

        def dem1():
            p=plot(aa-bb*x,(x,-5,aa/bb+5))
            return p
        def resd(d):
            d=sympify(d)
            res["x"]=[str(d)]
            return 


        display(HTML("<h3>Segundo ejercicio: </h3> <p>Mensualmente una compañía puede vender $x$ unidades de cierto artículo a $p$ pesos cada uno, en donde la relación entre $p$ y $x$ (precio y número de artículos vendidos) está dada por la siguiente ecuación: $"+str(latex(Eq(ppp,aa-bb*x)))+"$ ¿Cuántos artículos debe vender para obtener unos ingresos de $"+str(latex((xx*(aa-bb*xx))))+"$ dólares?</p><p></p><p></p>"))

        d5=interactive(dem1)

        display(d5)
        
        display(HTML("<p> Solución: Se deben vender:</p> "))
        
        
        def itemD():
            display(HTML("<p>$(a).$ Ingrese la cantidad de productos:</p><p></p><p></p>"))
            d1=interactive(resd,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            display(d1)
            return 

        a=itemD()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                nombrearchivo2="p2"+img_name
                p2= open(nombrearchivo2, "wb")
                p2.write(upload_file[img_name]["content"])
                p2.close()
                ra=latex(sympify(res["x"][0]))
                R2="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el segundo ejercicio son:</h3>"+ "<p>$x ="+ra+" $</p></div>"
                display(HTML(R2))
                RES["R2"]=R2  
                archivos["2"]=nombrearchivo2
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
    
    
    
    def Ejercicio3():

        def rese(d):
            d=sympify(d)
            res["renta"]=[str(d)]
            return 
        def resf(d):
            d=sympify(d)
            res["hab"]=[str(d)]
            return
        def resg(d):
            d=sympify(d)
            res["aumentos"]=[str(d)]
            return 

        display(HTML("<h3>Tercer ejercicio: </h3> <p>Carlos tiene un edificio con $"+str(latex(numhab))+"$ habitaciones. Si Carlos cobra por concepto de renta mensual $" +str(latex(renta))+"$ dólares por cada habitación, entonces todas las habitaciones son rentadas.Sin embargo, por cada $" +str(latex(aumento))+"$ dólares que le incremente a la renta de cada habitación se tendrán $"+str(latex(habvac))+"$ habitaciones desocupadas sin posibilidad de rentarlas. Si Carlos quiere recibir $ "+str(latex(ingresos))+ "$ por concepto de renta, ¿cuál debe ser la renta mensual de cada habitación?</p><p></p><p></p>"))
        
        
        
        def itemE():
            display(HTML("<p>$(a).$ Ingrese el precio de renta de cada habitación:</p><p></p><p></p>"))
            d1=interactive(rese,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            
            display(d1)
            return 

        def itemF():
            display(HTML("<p>$(a).$ Ingrese el número de habitaciones rentadas:</p><p></p><p></p>"))
            d1=interactive(resf,d=widgets.FloatText(
                value=0,
                description='$y = $ '
            ))  
            
           
            display(d1)
            return 
        
        def itemG():
            display(HTML("<p>$(a).$ Ingrese el número de aumentos:</p><p></p><p></p>"))
            d1=interactive(resg,d=widgets.FloatText(
                value=0,
                description='$z = $ '
            ))  
            
           
            display(d1)
            return 
        
        
        a=itemE()
        b=itemF()
        c=itemG()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                nombrearchivo3="p3"+img_name
                p3= open(nombrearchivo3, "wb")
                p3.close()
                ra=latex(sympify(res["renta"][0]))
                rb=latex(sympify(res["hab"][0]))
                rc=latex(sympify(res["aumentos"][0]))
                R3="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el tercer ejercicio son:</h3>"+ "<p>Renta ="+ra+"</p><p>Habitaciones ="+rb+" $</p><p>Aumentos ="+rc+" $</p></div>"
                display(HTML(R3))
                RES["R3"]=R3       
                archivos["3"]=nombrearchivo3
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
    
    
    
    def Ejercicio4():

        def resf(d):
            d=sympify(d)
            res["personas"]=[str(d)]
            return 
        def resg(d):
            d=sympify(d)
            res["sillas"]=[str(d)]
            return
        def resh(d):
            d=sympify(d)
            res["precio"]=[str(d)]
            return 

        display(HTML("<h3>Cuarto ejercicio: </h3> <p>En un vuelo privado con capacidad para $"+str(latex(personas))+"$ personas se cobra $"+str(latex(precio)) +"$ pesos por persona más $"+str(latex(preciosillavacia))+"$ pesos por cada silla no vendida en el avión, ¿Cuántas personas deben viajar en el avión y cuál será el precio de cada boleto de avión si se requieren unos ingresos de $"+ str(latex(ingresosav))+"$ de pesos</p><p></p><p></p>"))
        
        
        
        def itemF():
            display(HTML("<p>$(a).$  Ingrese la cantidad de personas que deben viajar:</p><p></p><p></p>"))
            d1=interactive(resf,d=widgets.FloatText(
                value=0,
                description='$x = $ '
            ))  
            
            display(d1)
            return 

        def itemG():
            display(HTML("<p>$(b).$ Ingrese el número de sillas vacías:</p><p></p><p></p>"))
            d1=interactive(resg,d=widgets.FloatText(
                value=0,
                description='$y = $ '
            ))  
            
           
            display(d1)
            return 
        
        def itemH():
            display(HTML("<p>$(c).$ Ingrese el precio del boleto:</p><p></p><p></p>"))
            d1=interactive(resh,d=widgets.FloatText(
                value=0,
                description='$z = $ '
            ))  
            
           
            display(d1)
            return 
        
        
        a=itemF()
        b=itemG()
        c=itemH()
        
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                nombrearchivo4="p4"+img_name
                p4= open(nombrearchivo4, "wb")
                p4.write(upload_file[img_name]["content"])
                p4.close()
                ra=res["personas"][0]
                rb=res["sillas"][0]
                rc=res["precio"][0]
                R4="<div style='background-color:Teal;color:White;'> <h3>Sus respuestas para el cuarto ejercicio son:</h3><p>Personas ="+ra+"</p><p>Sillas ="+rb+" </p><p>Precios ="+rc+" </p></div>"
                display(HTML(R4))
                RES["R4"]=R4
                archivos["4"]=nombrearchivo4
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
            display(HTML("<h3>Quinto ejercicio: </h3> <p> Sobre la carpeta en la que ejecuta el cuaderno después de clickear el botón generar"
                     "encontrará una base de datos que recoge información de 500 personas respecto a su talla de calzado. Haga un informe exploratorio"
                     " con las herramientas vistas en el curso de dicha base.</p><p></p><p></p>"))
            def generarzap(B):
                try:
                    Obs=500
                    df = pd.DataFrame({'Edad': np.random.randint(20, 70, Obs),
                                       'Sexo': np.random.choice(['Masculino', 'Femenino'], Obs),
                                       'Talla de zapato': np.random.randint(20, 45, Obs)})
                    df.to_excel("Zapatos.xlsx")               
                except:
                    display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
     
            
            def guardar(B):
                try:
                    df=pd.DataFrame(res)
                    df.to_csv("prueba.csv")        
                    upload_file=Upload.value        
                    img_name=list(upload_file.keys())[0]
                    nombrearchivo5="p5"+img_name
                    p5= open(nombrearchivo5, "wb")
                    p5.write(upload_file[img_name]["content"])
                    p5.close()   
                    archivos["5"]=nombrearchivo5
                except:
                    display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))


            BG=widgets.Button(
                description='Generar',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Generar Zapatos.xlsx',
                icon='check' # (FontAwesome names without the `fa-` prefix)
            )
            BG.on_click(generarzap)                  

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
                accept='.xls,.xlsx,.doc,.docx',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
                multiple=True  # True to accept multiple files upload else False
            )
            display(BG)

            display(HTML("<p>Ingrese aquí un soporte del ejercicio:</p>"))
            display(Upload)
            display(HTML("<p>Guarde sus respuestas</p>"))
            display(B)
            return    

    def Ejercicio6():


        display(HTML("<h3>Sexto ejercicio: </h3> <p> Sobre la carpeta en la que ejecuta el cuaderno después de clickear el botón generar"
                     "encontrará una base de datos que recoge información de 1000 calificaciones a diferentes personas. Haga un informe exploratorio"
                     " con las herramientas vistas en el curso de dicha base.</p><p></p><p></p>"))
        
        
        
        def generarnot(B):
            try:
                Obs=1000
                df = pd.DataFrame({
                    'Edad': np.random.randint(15, 10**2 - 70, Obs),
                    'Código': [i+100000 for i in range(Obs)],
                    'Nota': np.random.rand(Obs)*5,
                }) 
                df.to_excel("Notas.xlsx")               
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
     
            
        def guardar(B):
            try:
                df=pd.DataFrame(res)
                df.to_csv("prueba.csv")        
                upload_file=Upload.value        
                img_name=list(upload_file.keys())[0]
                nombrearchivo6="p6"+img_name
                p6= open(nombrearchivo6, "wb")
                p6.write(upload_file[img_name]["content"])
                p6.close()    
                archivos["6"]=nombrearchivo6
            except:
                display(HTML("<div style='background-color:Tomato;color:White;'> <h3>¡No olvide subir el soporte!</h3>"))
            
                        
        BG=widgets.Button(
            description='Generar',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Generar Notas.xlsx',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        BG.on_click(generarnot)                  
                                           
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
            accept='.xls,.xlsx,.doc,.docx',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=True  # True to accept multiple files upload else False
        )
        display(BG)

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
                message="""<html><head></head><body><p>El alumno con identificación"""+str(n)+""" envía lo siguiente:</p> """+RES["R1"]+RES["R2"]+RES["R3"]+RES["R4"]+"""</body></html>"""
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
                    attachments=[filename,archivos["1"],archivos["2"],archivos["3"],archivos["4"],archivos["5"],archivos["6"],"prueba.csv"],
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

