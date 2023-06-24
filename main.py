from calculadora import Calculadora
from src.label import LabelText
from src.input import Input
from src.calculadora import Calculadora
import pygame as py
import sys

def main():
    calculadora = Calculadora()
    calculadora.add_constante('a', 7.5)
    # calculadora.delete_constante('a')
    print(calculadora.evaluar('a+3'))

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
    label = LabelText('F(x)', 'grey', (100, 100), (0, 0))

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

        # Darle color al fondo
        screen.fill('black')
        canvas.fill('white')
        
        # Dibujar el label en el canvas
        label.draw(canvas, font)

        # Dibujar el canvas en la pantalla
        # Ultimo en dibujar, para que se vea debajo de todo
        screen.blit(canvas, (0, 0))
        py.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
