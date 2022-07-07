import tkinter as tk
import math


'''
10Hz -> periodo
20Hz en cambio de color del rectangulo
cada 50ms(20Hz) debe cambiar el color del rectangulo

8hz -> cambio cada 16hz(62ms aprox)
10hz -> cambio cada 20hz(50ms)
12hz -> cambio cada 24hz(41ms aprox)
15hz -> cambio cada 30hz(33ms aprox)
'''


class flicker:

    flick_id = None
    flickTimer = [0,0,0,0]
    freqs = [62,50,41,33]
    max_loop = [math.ceil(5000/freqs[0])+1,math.ceil(5000/freqs[1]),math.ceil(5000/freqs[2]),math.ceil(5000/freqs[3])]
    flickerObjetivo= ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]

    def prox_rectangulo(self,texto,canvas, window):
        textID = canvas.create_text(0,0, text=texto, anchor="nw", fill="black",font=('Times','45'))
        coords = canvas.bbox(textID)
        xOffset = (window.winfo_screenwidth()/ 2) - ((coords[2] - coords[0]) / 2)
        canvas.move(textID, xOffset, 375)
        return textID
    
    def destroy_tk(self, window):
        window.quit()
    
    def destroy_canvas(self,canvas):
        canvas.delete('all')
    
    def flickRectangs(self,_canvas,rectang, time, timer, max_loop, window):
        timer += 1
        if(_canvas.itemcget(rectang,'fill')!='black'):
            _canvas.itemconfig(rectang, fill='black')
            _canvas.itemconfig(rectang, outline='black')
        else:
            _canvas.itemconfig(rectang, fill='white')
            _canvas.itemconfig(rectang, outline='white')
        
        if(timer== max_loop):
            timer = 0
            window.after_cancel(self.flick_id)
        else:
            window.after(time,self.flickRectangs,_canvas,rectang,time,timer,max_loop,window)
    
    def start_flickers(self,canvas, rectangs, window,startDataAdq, l):
        l.acquire()
        startDataAdq.value = True
        l.release()
        for indexRectang in range(len(rectangs)):
            self.flickRectangs(canvas,rectangs[indexRectang],self.freqs[indexRectang], self.flickTimer[indexRectang], self.max_loop[indexRectang], window)
        window.after(5100, self.destroy_canvas, canvas)
        window.after(9000, self.destroy_tk, window)

    def destroy_text(self,textID,_canvas):
        _canvas.delete(textID)

    def runPrueba(self,startDataAdq, l, loop):
        window = tk.Tk()
        window.configure(cursor='none')

        # setting attribute
        window.attributes('-fullscreen', True)

        _canvas = tk.Canvas(window,bg='white')
        _canvas.pack(fill=tk.BOTH,expand=True)

        # create rectangle
        rect1 = _canvas.create_rectangle(25,25, 515, 300,outline="white",fill="white")
        rect2 = _canvas.create_rectangle(1021,25, 1511, 300,outline="white",fill="white")
        rect3 = _canvas.create_rectangle(25,564, 515, 839,outline="white",fill="white")
        rect4 = _canvas.create_rectangle(1021,564, 1511, 839,outline="white",fill="white")

        rectangs = [rect1, rect2, rect3, rect4]

        textID = self.prox_rectangulo(self.flickerObjetivo[loop%4],_canvas, window)
        window.after(3000, self.destroy_text,textID,_canvas)
        self.flick_id = window.after(3000,self.start_flickers,_canvas,rectangs, window,startDataAdq, l)
        
        window.mainloop()
    
    def runBloque(self,startDataAdq, l,n_pruebas):
        for loop in range(n_pruebas):
            self.runPrueba(startDataAdq, l, loop)
    
    def checkPositions(self):
        window = tk.Tk()
        window.configure(cursor='none')

        # setting attribute
        window.attributes('-fullscreen', True)

        _canvas = tk.Canvas(window,bg='white')
        _canvas.pack(fill=tk.BOTH,expand=True)

        """ rect1 = _canvas.create_rectangle(50,307, 450, 557,outline="black",fill="black")
        rect3 = _canvas.create_rectangle(568,50, 968, 300,outline="black",fill="black")
        rect2 = _canvas.create_rectangle(1086,307, 1486, 557,outline="black",fill="black")
        rect4 = _canvas.create_rectangle(568,564, 968, 814,outline="black",fill="black") """

        rect1 = _canvas.create_rectangle(25,25, 515, 300,outline="black",fill="black")
        rect2 = _canvas.create_rectangle(1021,25, 1511, 300,outline="black",fill="black")
        rect3 = _canvas.create_rectangle(25,564, 515, 839,outline="black",fill="black")
        rect4 = _canvas.create_rectangle(1021,564, 1511, 839,outline="black",fill="black")

        window.mainloop()

if __name__=="__main__":
    s = flicker()
    s.checkPositions()

