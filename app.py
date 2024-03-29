import sys
import tkinter as tk
import numpy as np
from tkinter import ttk

poly_creator = np.polynomial.polynomial
polinomio_interpolacion = []
puntosx = []
puntosy = []
estaElPunto00 = False


class PrintLogger():
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)

    def flush(self):
        pass


class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("FINTER")

        self.points = []
        self.xValue = tk.IntVar()
        self.yValue = tk.IntVar()

        self.xLabel = tk.Label(self, text="Valor x")
        self.xLabel.pack()

        self.xInput = tk.Entry(self, text="Valor x", textvariable=self.xValue)
        self.xInput.pack()

        self.yLabel = tk.Label(self, text="Valor y")
        self.yLabel.pack()

        self.yInput = tk.Entry(self, text="Valor y", textvariable=self.yValue)
        self.yInput.pack()

        self.addButton = tk.Button(self, text="Agregar punto", command=self.addPoint)
        self.addButton.configure(pady=10)
        self.addButton.pack()

        self.removeButton = tk.Button(self, text="Sacar punto", command=self.removePoint)
        self.removeButton.configure(pady=10)
        self.removeButton.pack()

        # Log points
        self.puntosListbox = tk.Listbox(self)
        self.puntosListbox.pack()

        self.methodsLabel = tk.Label(self, text="Metodos de calculo")
        self.methodsLabel.pack()

        self.methods = ["Lagrange", "Newton-Gregory progresivo", "Newton-Gregory regresivo"]
        self.methodCombo = ttk.Combobox(self, values=self.methods)
        self.methodCombo.pack()

        self.checkButtonValue = tk.IntVar()
        self.checkButton = tk.Checkbutton(self, text="Mostrar pasos de calculo", variable=self.checkButtonValue)
        self.checkButton.pack()

        self.kValue = tk.IntVar()

        self.evalPoliLabel = tk.Label(self, text="Especializar el polinomio en valor K")
        self.evalPoliLabel.pack()

        self.evalPoliInput = tk.Entry(self, text="Valor K", textvariable=self.kValue)
        self.evalPoliInput.pack()

        self.calcButton = tk.Button(self, text="Calcular polinomio interpolante", command=self.calculateInterpolator)
        self.calcButton.configure(pady=10)
        self.calcButton.pack()

        # Log to screen
        self.logText = tk.Text(self)
        self.logText.pack()

        pl = PrintLogger(self.logText)
        sys.stdout = pl

        main_window.configure(pady=20, padx=50)
        self.pack()

    def addPoint(self):
        point_to_add = {'x': self.xValue.get(), 'y': self.yValue.get()}
        if {point_to_add['x']} == {0} and {point_to_add['y']} == {0}:
            global estaElPunto00
            estaElPunto00 = True
        if point_to_add in self.points:
            print(f"Ya agrego el punto ({point_to_add['x']}, {point_to_add['y']})")
        else:
            def take_x(_point):
                return _point['x']

            self.points.append(point_to_add)
            self.points.sort(key=take_x)

            global puntosx
            puntosx = list(map(lambda _point: _point['x'], self.points))

            global puntosy
            puntosy = list(map(lambda _point: _point['y'], self.points))

            self.puntosListbox.delete(0, tk.END)

            for point in self.points:
                self.puntosListbox.insert(tk.END, f"({point['x']}, {point['y']})")

    def removePoint(self):
        if not self.points:
            print("No hay puntos que borrar")
        elif not self.puntosListbox.curselection():
            print("No ha seleccionado ningun punto")
        else:
            point = self.puntosListbox.get(self.puntosListbox.curselection()) \
                .replace('(', '') \
                .replace(')', '') \
                .replace(',', '') \
                .split()

            self.points = [
                p for p in self.points if p['x'] != float(point[0]) or p['y'] != float(point[1])
            ]

            self.puntosListbox.delete(self.puntosListbox.curselection())

            global puntosx
            puntosx = list(map(lambda p: p['x'], self.points))

            global puntosy
            puntosy = list(map(lambda p: p['y'], self.points))

    def calculateInterpolator(self):
        # TODO guille aca esta el valor del checkbox
        hayQueMostrarCalculos = self.checkButtonValue.get()
        if len(self.points) == 0:
            print("Por favor ingrese puntos para sacar un polinomio interpolante")
        else:
            print("\nCalculando por", self.methodCombo.get(), "para puntos:", self.points);
            if self.methodCombo.get() == "Lagrange":
                armarPolinomioInterpolanteLAG(hayQueMostrarCalculos)  # TODO cambiar esto por lo que dice la checkbox
                evaluarPolinomioInterpolanteEn(self.kValue.get())

            if self.methodCombo.get() == "Newton-Gregory progresivo":
                sacarPolinomioProgresivo(sacarCoeficientesLagrange(puntosx, puntosy, hayQueMostrarCalculos),
                                         hayQueMostrarCalculos)  # TODO cambiar los booleanos por lo que dice la checkbox
                evaluarPolinomioInterpolanteEn(self.kValue.get())

            if self.methodCombo.get() == "Newton-Gregory regresivo":
                sacarPolinomioRegresivo(sacarCoeficientesLagrange(puntosx, puntosy, hayQueMostrarCalculos),
                                        hayQueMostrarCalculos)  # TODO cambiar los booleanos por lo que dice la checkbox
                evaluarPolinomioInterpolanteEn(self.kValue.get())
            pass


def sacarCoeficientesLagrange(puntos_x, puntos_y, hayQueMostrarCalculos):
    cantidad_puntos = len(puntos_x);
    matriz_coeficientes = [[0 for x in range(cantidad_puntos)] for y in range(cantidad_puntos + 1)]
    cantidad_iteraciones = cantidad_puntos - 2
    for i in range(cantidad_puntos):  # meto los puntos iniciales a la matriz  de coeficientes
        matriz_coeficientes[0][i] = puntos_x[i]
        matriz_coeficientes[1][i] = puntos_y[i]
    numerosAMostrar = ""
    if cantidad_puntos > 1:
        for i in range(cantidad_puntos - 1):
            matriz_coeficientes[2][i] = (matriz_coeficientes[1][i + 1] - matriz_coeficientes[1][i]) / (
                        matriz_coeficientes[0][i + 1] - matriz_coeficientes[0][i])
            numerosAMostrar = numerosAMostrar + str(matriz_coeficientes[2][i]) + ", "
    if hayQueMostrarCalculos:
        print("\nLos valores ꕔ1" + " Son: " + numerosAMostrar)
    if cantidad_puntos > 2:
        for i in range(3, cantidad_puntos + 1):
            numerosAMostrar = ""
            for j in range(cantidad_iteraciones):
                matriz_coeficientes[i][j] = (matriz_coeficientes[i - 1][j + 1] - matriz_coeficientes[i - 1][j]) / (
                            matriz_coeficientes[0][i - 1 + j] - matriz_coeficientes[0][j])
                numerosAMostrar = numerosAMostrar + str(matriz_coeficientes[i][j]) + ", "
            cantidad_iteraciones = cantidad_iteraciones - 1
            if hayQueMostrarCalculos:
                print("Los valores ꕔ" + str(i - 1) + " Son: " + numerosAMostrar)
    return matriz_coeficientes


def sacarPolinomioProgresivo(matriz_coeficientes, hayQueMostrarCalculos):
    coeficientes_progresivo = [];
    for i in range(len(puntosx)):
        coeficientes_progresivo.append(matriz_coeficientes[i + 1][0])
    if hayQueMostrarCalculos:
        print("\nLos coeficientes del polinomio progresivo son: " + str(coeficientes_progresivo))
    armarPolinomioInterpolanteNGPROG(coeficientes_progresivo)


def sacarPolinomioRegresivo(matriz_coeficientes, hayQueMostrarCalculos):
    coeficientes_progresivo = [];
    for i in range(len(puntosx)):
        coeficientes_progresivo.append(matriz_coeficientes[i + 1][len(puntosx) - 1 - i])
    if hayQueMostrarCalculos:
        print("\nLos coeficientes del polinomio Regresivo son: " + str(coeficientes_progresivo))
    armarPolinomioInterpolanteNGREG(coeficientes_progresivo)


def armarPolinomioInterpolanteNGPROG(coeficientes):
    polinomioDeRaices = [1]
    polinomioDeRaices = np.resize(polinomioDeRaices, 1)
    polinomioInterpolante = [0]
    cantidadPuntos = len(coeficientes)

    for i in range(len(coeficientes) - 1):
        polinomioRaicesDeEstaIteracion = poly_creator.polyfromroots([puntosx[i]])
        poli1 = poly_creator.polymulx(polinomioDeRaices)
        poli2 = polinomioDeRaices * polinomioRaicesDeEstaIteracion[0]

        for q in range(len(poli2)):
            poli1[q] = poli1[q] + poli2[q]
        polinomioDeRaices = poli1

        polinomioDeIteracion = polinomioDeRaices * coeficientes[i+1]


        for j in range(i + 1):
            polinomioDeIteracion[j] = polinomioDeIteracion[j] + polinomioInterpolante[j]
        polinomioInterpolante = polinomioDeIteracion

    polinomioInterpolante[0] = polinomioInterpolante[0] + coeficientes[0]

    mostrarPoliniomio(polinomioInterpolante, cantidadPuntos)
    polinomioInterpolante = voltearArray(polinomioInterpolante, cantidadPuntos)
    global polinomio_interpolacion
    polinomio_interpolacion = polinomioInterpolante


def armarPolinomioInterpolanteNGREG(coeficientes):
    polinomioDeRaices = [1]
    polinomioInterpolante = [0]
    cantidadPuntos = len(coeficientes)
    for i in range(len(coeficientes) - 1):
        if puntosx[(len(coeficientes) - 1 - i)] == 0:
            polinomioDeRaices = poly_creator.polymulx(polinomioDeRaices)
        else:
            if polinomioDeRaices[0] == 0 and polinomioDeRaices[1] == 1 and len(polinomioDeRaices) == 2:
                polinomioDeRaices = poly_creator.polymulx(
                    poly_creator.polyfromroots([puntosx[(len(coeficientes) - 1 - i)]]))
            else:
                polinomioDeRaices = np.polymul(polinomioDeRaices,
                                               poly_creator.polyfromroots([puntosx[(len(coeficientes) - 1 - i)]]))

        polinomioDeIteracion = coeficientes[i + 1] * polinomioDeRaices
        polinomioDeIteracion = np.array(polinomioDeIteracion)
        for j in range(i + 1):
            polinomioDeIteracion[j] = polinomioDeIteracion[j] + polinomioInterpolante[j]
        polinomioInterpolante = polinomioDeIteracion

    polinomioInterpolante[0] = polinomioInterpolante[0] + coeficientes[0]
    mostrarPoliniomio(polinomioInterpolante, cantidadPuntos)
    polinomioInterpolante = voltearArray(polinomioInterpolante, cantidadPuntos)
    global polinomio_interpolacion
    polinomio_interpolacion = polinomioInterpolante


def armarPolinomioInterpolanteLAG(hayQueMostrarCalculos):
    polinomioInterpolante = [0]
    polinomioInterpolante = np.resize(polinomioInterpolante, len(puntosy))
    cantidadPuntos = len(puntosy)
    for i in range(len(puntosy)):
        polinomioDeIteracion = [1]
        polinomioDeIteracion = np.resize( polinomioDeIteracion, len(puntosy))
        for j in range(len(puntosy)):
            if i == j:
                pass
            else:

                numerador = poly_creator.polyfromroots([puntosx[j]])
                denominador = puntosx[i] - puntosx[j]

                poli1 = polinomioDeIteracion * numerador[1]
                poli1 = poly_creator.polymulx(poli1)
                poli2 =  polinomioDeIteracion * numerador[0]

                for q in range(len(poli2)):
                    poli1[q] = poli2[q] + poli1[q]

                poli1 = poli1 * (1/denominador)
                polinomioDeIteracion = poli1

        if hayQueMostrarCalculos:
            mostrarLn(polinomioDeIteracion, len(puntosy), i)
        polinomioDeIteracion = polinomioDeIteracion * puntosy[i]
        polinomioDeIteracion = np.array(polinomioDeIteracion)
        if puntosx[i] == 0:
            pass
        else:
            for q in range(cantidadPuntos):
                polinomioDeIteracion[q] = polinomioDeIteracion[q] + polinomioInterpolante[q]
        polinomioInterpolante = polinomioDeIteracion
    sacarPolinomioProgresivo(sacarCoeficientesLagrange(puntosx, puntosy, False), False)


def voltearArray(arrayAVoltear, longitudArray):
    arrayVolteado = []
    for i in range(longitudArray):
        arrayVolteado.append(arrayAVoltear[longitudArray - i - 1])
    return arrayVolteado


def mostrarPoliniomio(array, longitudArray):
    polinomio = str(array[0])
    for i in range(1, longitudArray):
        polinomio = polinomio + " + " + str(array[i]) + "x^" + str(i)
    print("\nEl polinomio de interpolacion es:")
    print(polinomio)


def mostrarLn(array, longitudArray, n):
    polinomio = str(array[0])
    for i in range(1, longitudArray):
        polinomio = polinomio + " + " + str(array[i]) + "x^" + str(i)
    print("\nEl valor de L" + str(n) + " es: " + str(polinomio))


def evaluarPolinomioInterpolanteEn(x):
    if len(polinomio_interpolacion) == 0:
        print("\nPor favor primero cree el polinomio interpolante antes de intentar evaluar en algun punto")
    else:
        valor = np.polyval(polinomio_interpolacion, x)
        print("\nEl valor del polinomio interpolante en el punto " + str(x) + " es: " + str(valor))


if __name__ == '__main__':
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
