from interfaz import *
from util import *

class ComandosCons:
    calculadora = None
    info_canvas = None
    input_text = None
    input_color = None
    input_rango_var1 = None
    input_rango_var2 = None
    slider_rebanada = None
    slider_vector = None
    axis_button = None
    coord_button = None
    dim_button = None
    long_button = None
    flujo_button = None
    g = None
    g3 = None


def mostrar_info():
    info_canvas = ComandosCons.info_canvas
    calculadora = ComandosCons.calculadora
    i=0
    for obj in info_canvas.objetos:
        if isinstance(obj, InfoLabel) or isinstance(obj, DeleteBoton):
            obj.kill()
    info_canvas.objetos.clear()
    for tipo_grafico in calculadora.get_grafics():
            for name_grafic in calculadora.get_grafics()[tipo_grafico]:
                grafic = calculadora.get_grafics()[tipo_grafico][name_grafic]
                info = InfoLabel((400, 60), (0,i*120), name_grafic, grafic)
                delete_boton = DeleteBoton((100, 30), (150, 90+120*i), name_grafic, command=delete)
                info_canvas.add(info, delete_boton)
                i+=1

    
    for name_parametro in calculadora.get_parametros():
        parametro = calculadora.get_parametros()[name_parametro]
        info = InfoLabel((400, 60), (0,i*120), name_parametro, parametro)
        delete_boton = DeleteBoton((100, 30), (150, 90+120*i), name_parametro, command=delete)
        run_boton = DeleteBoton((100, 30), (0, 90+120*i), name_parametro, command=run, text='Run')
        slider = Slider((100, 30), (150,i*120 + 50),parametro.porcentaje, name_parametro, velocidad=parametro.velocidad)
        info_canvas.add(info, delete_boton, slider, run_boton)
        i+=1

def apply(): #Arreglar colores que no existen
    input_text = ComandosCons.input_text
    input_color = ComandosCons.input_color
    input_rango_var1 = ComandosCons.input_rango_var1
    input_rango_var2 = ComandosCons.input_rango_var2
    slider_rebanada = ComandosCons.slider_rebanada
    slider_vector = ComandosCons.slider_vector
    calculadora = ComandosCons.calculadora
    try:
        text = input_text.get_text().replace(" ", "")
        color = input_color.get_text().replace(" ", "")
        rango1 = input_rango_var1.get_text().replace(" ", "")
        rango2 = input_rango_var2.get_text().replace(" ", "")
        input_text.clear()
        input_color.clear()
        input_rango_var1.clear()
        input_rango_var2.clear()
        if text != "":
            if '=' in text:
                name, exp = text.split('=')
                tipo = identificar_tipo_entrada(exp)
            else:
                exp = text
                tipo = identificar_tipo_entrada(exp)
                name = nombre_default(tipo)
            
            if color == '':
                color = 'orange'
            
            rebanadas = slider_rebanada.get_porcentaje()
            long_vector = slider_vector.get_porcentaje()
            calculadora.gen_grafic(tipo, name, color, exp, rebanadas, long_vector, rango1, rango2)
            mostrar_info()
    except:
        pass

def update():
    calculadora = ComandosCons.calculadora
    info_canvas = ComandosCons.info_canvas
    for tipo_grafico in calculadora.get_grafics():
        for name_grafic in calculadora.get_grafics()[tipo_grafico]:
            grafic = calculadora.get_grafics()[tipo_grafico][name_grafic]
            grafic.info = grafic.load_info()
    for info in info_canvas.objetos:
        if isinstance(info, InfoLabel):
            info.set_text(f"{info.name} = {info.obj}")


def delete(name):
    info_canvas = ComandosCons.info_canvas
    calculadora = ComandosCons.calculadora
    calculadora.delete(name)
    for obj in info_canvas.objetos:
        if isinstance(obj, InfoLabel) or isinstance(obj, DeleteBoton):
            if obj.name == name:
                obj.kill()
                mostrar_info()
def run(name):
    info_canvas = ComandosCons.info_canvas
    for obj in info_canvas.objetos:
        if isinstance(obj, DeleteBoton) and obj.name == name:
            if obj.text == 'Run':
                obj.set_text('Stop')
            elif obj.text == 'Stop':
                obj.set_text('Run')
        if isinstance(obj, Slider):
            if obj.name_parametro == name:
                obj.set_velocidad()
                obj.correr()

                
def axis():
    axis_button = ComandosCons.axis_button
    calculadora = ComandosCons.calculadora
    if axis_button.text == 'Axis 1':
        axis_button.set_text('Axis 2')
        calculadora.set_axis(2)
    
    elif axis_button.text == 'Axis 2':
        axis_button.set_text('Axis 3')
        calculadora.set_axis(3)
    else:
        axis_button.set_text('Axis 1')
        calculadora.set_axis(1)

def coord():
    coord_button = ComandosCons.coord_button
    calculadora = ComandosCons.calculadora
    if coord_button.text == 'Cartesiano':
        coord_button.set_text('Esfera')
        calculadora.set_mode('Esfera')

    elif coord_button.text == 'Esfera':
        coord_button.set_text('Cilindro')
        calculadora.set_mode('Cilindro')
    
    else:
        coord_button.set_text('Cartesiano')
        calculadora.set_mode('Cartesiano')

def dim():
    dim_button = ComandosCons.dim_button
    g = ComandosCons.g
    g3 = ComandosCons.g3
    if dim_button.text == '2D':
        dim_button.set_text('3D')
        g.set_visible(False)
        g3.set_visible(True)
    else:
        dim_button.set_text('2D')
        g3.set_visible(False)
        g.set_visible(True)

def magitud_vector():
    calculadora = ComandosCons.calculadora
    long_button = ComandosCons.long_button
    if long_button.text == 'Unitario':
        long_button.set_text('Default')
        calculadora.set_unitario(False)
    else:
        long_button.set_text('Unitario')
        calculadora.set_unitario(True)

def flujo():
    calculadora = ComandosCons.calculadora
    flujo_button = ComandosCons.flujo_button
    if flujo_button.text == 'Flujo':
        flujo_button.set_text('Fuerza')
        calculadora.tipo_campo='Fuerza'
    else:
        flujo_button.set_text('Flujo')
        calculadora.tipo_campo='Flujo'
