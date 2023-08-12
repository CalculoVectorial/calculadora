import numpy as np
import pygame as py, sys
from globals_var import *





screen = py.display.set_mode(size)
fps = 60
clock = py.time.Clock()
while True:
    pressed = py.mouse.get_pressed()
    mouse = py.mouse.get_rel()
    pos = py.mouse.get_pos()
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
        
        if event.type == py.MOUSEWHEEL:
            g.zoom(event, pos)
            g3.zoom(event, pos)
        g.mouse_event(pressed, mouse, pos)
        g3.mouse_event(pressed, mouse, pos)
        manager.process_events(event) #Detecta eventos del for event, esta línea es OBLIGATORIA
                
    contain_canvas.click_event(pressed, mouse, pos)  #Detecta eventos de clicks para botones, esta línea es OBLIGATORIA
    
    screen.fill('black')
    contain_canvas.draw(screen) #Se dibuja el canvas en el screen
    g3.draw(calculadora.get_grafics())
    g.draw(calculadora.get_grafics())
    py.display.flip()
    manager.update(clock.tick(fps)/600) #Se actualiza el manager, esta línea es OBLIGATORIA
