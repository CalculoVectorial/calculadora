from src.calculadora import Calculadora
from src.label import LabelText
from src.input import InputText 
import pygame as py
import sys

def main():
    calculadora = Calculadora()
    calculadora.add_constante('a', 7.5)
    # calculadora.delete_constante('a')
    # print(calculadora.evaluar('a+3'))

    # Setup inicial del juego, boilerplate
    py.init()
    size = (850, 480)
    screen = py.display.set_mode(size)
    py.display.set_caption("Calculadora Gráfica")

    # Por buena practica, se dibuja encima del canvas
    canvas = py.Surface(size)

    # mas boilerplate
    fps = 60
    clock = py.time.Clock()

    # Para dibujar texto
    font = py.font.Font(None, 24)

    # LabelText, clase para dibujar texto con un rectangulo de fondo
    labels = []
    labels.append(LabelText('F(x)', 'grey', (100, 100), (0, 0)))

    # InputText, clase para entradas de texto, hereda de LabelText
    inputs = []
    inputs.append(InputText('', 'blue', (100,100), (0, 100), False, 'orange', 'green'))

    # texto del usuario
    user_text = ''

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                for input_text in inputs:
                    if input_text.clicked(event.pos):
                        input_text.setActive(True)
                    else:
                        input_text.setActive(False)
            
            if event.type == py.KEYDOWN: # se aplasta una tecla
                if event.key == py.K_BACKSPACE: # si se esta borrando datos 
                    user_text = user_text[:-1]
                else: # se agrega 
                    user_text += event.unicode
                        

        # Darle color al fondo
        screen.fill('black')
        canvas.fill('white')
        
        # Dibujar el label en el canvas
        for label in labels:
            label.draw(canvas, font)

        for input_text in inputs:
            input_text.draw(canvas, font, user_text)
            

        # Dibujar el canvas en la pantalla
        # Ultimo en dibujar, para que se vea debajo de todo
        screen.blit(canvas, (0, 0))
        py.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
