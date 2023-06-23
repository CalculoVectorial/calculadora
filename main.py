from calculadora import Calculadora

def main():
    calculadora = Calculadora()
    calculadora.add_constante('a', 7.5)
    calculadora.delete_constante('a')
    print(calculadora.evaluar('a+3'))

main()