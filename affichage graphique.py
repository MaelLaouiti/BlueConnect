# coding: utf-8
 
from tkinter import * 

fenetre = Tk()
fenetre['bg']='white'
fenetre.geometry("800x480")
fenetre.title("Blue Connect")

###################Affichage données
# Creating labels
label1 = Label(fenetre, text="Hum.", width=10, height=2)
label2 = Label(fenetre, text="Lum.", width=10, height=2)
label3 = Label(fenetre, text="XX% H", width=10, height=2)
label4 = Label(fenetre, text="XX Lum", width=10, height=2)
label5 = Label(fenetre, text="LUX", width=10, height=2)
label6 = Label(fenetre, text="Temp.", width=10, height=2)
label7 = Label(fenetre, text="XX°C", width=10, height=2)
label8 = Label(fenetre, text="Temp. cible", width=10, height=2)
label9 = Label(fenetre, text="XX°C", width=10, height=2)
label10 = Label(fenetre, text="CO2", width=10, height=2)
label11 = Label(fenetre, text="XX", width=10, height=2)
label12 = Label(fenetre, text="PPM", width=10, height=2)

# Placing labels using grid layout
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)
label3.grid(row=1, column=0)
label4.grid(row=1, column=1)
label5.grid(row=2, column=1)
label6.grid(row=3, column=0)
label7.grid(row=4, column=0)
label8.grid(row=3, column=1)
label9.grid(row=4, column=1)
label10.grid(row=0, column=3)
label11.grid(row=1, column=3)
label12.grid(row=2, column=3)

fenetre.mainloop()