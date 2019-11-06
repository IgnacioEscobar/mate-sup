import sys
import tkinter as tk
from tkinter import ttk

lista = []

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
      
    def calculateInterpolator(self):
      print("Calculando por", self.methodCombo.get() ,"para puntos:", self.points)
      pass

if __name__ == '__main__':
  main_window = tk.Tk()
  app = Application(main_window)
  app.mainloop()