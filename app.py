import sys
import tkinter as tk
from tkinter import ttk

puntosx = [];
puntosy = [];

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

      self.methods = ["Lagrange", "Newton-Gregory progresivo", "Newton-Gregory regresivo"]
      self.methodCombo = ttk.Combobox(self, values=self.methods)
      self.methodCombo.pack()

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
      self.points.append({'x': self.xValue.get(), 'y': self.yValue.get()})
      puntosx.append(self.xValue.get())
      puntosy.append(self.yValue.get())
      
    def calculateInterpolator(self):
        print("Calculando por", self.methodCombo.get(), "para puntos:", self.points);
        if self.methodCombo.get() == "Lagrange":
            print("Aca hago cosas de lagrange");
        else :
            if self.methodCombo.get() == "Newton-Gregory progresivo": sacarCoeficientesLagrange(puntosx,puntosy);
            else: print("Aca hago cosas de Newton-Gregory regresivo");
        pass

def sacarCoeficientesLagrange (puntos_x,puntos_y):
    cantidad_puntos = len(puntos_x);
    matriz_coeficientes = [[0 for x in range(cantidad_puntos)] for y in range(cantidad_puntos+1)]
    cantidad_iteraciones = cantidad_puntos -2
    for i in range(cantidad_puntos): #meto los puntos iniciales a la matriz  de coeficientes
        matriz_coeficientes[0][i] = puntos_x[i]
        matriz_coeficientes[1][i] = puntos_y[i]

    if cantidad_puntos > 1 :
        for i in range(cantidad_puntos-1):
            matriz_coeficientes[2][i] = (matriz_coeficientes[1][i+1] - matriz_coeficientes[1][i])/(matriz_coeficientes[0][i+1]-matriz_coeficientes[0][i])
            print(matriz_coeficientes[2][i])
    if cantidad_puntos > 2 :
        for i in range (3, cantidad_puntos+1):
            for j in range (cantidad_iteraciones):
                matriz_coeficientes[i][j] = (matriz_coeficientes[i - 1][j + 1] - matriz_coeficientes[i - 1][j]) / (matriz_coeficientes[0][i-1+j]-matriz_coeficientes[0][j])
                print(matriz_coeficientes[i][j])
            cantidad_iteraciones = cantidad_iteraciones - 1



if __name__ == '__main__':
  main_window = tk.Tk()
  app = Application(main_window)
  app.mainloop()

