import json
import time
from tkinter import *
from tkinter.ttk import Combobox

import numpy as np

prev_x = None
prev_y = None
res_points = None
res_velocity = None
res_coeff = None
Plane = []
point1 = {}
point2 = {}
ImitationRequest = ''
ImitationResponse = ''
isUsualHit = 'red'
isFuzzyHit = 'red'


def requestPointToNPPoint(p):
    return np.array([[p['x']], [p['y']]], np.float64)


def start():
    global res_points
    global res_velocity
    global res_coeff
    global Plane
    global point1
    global point2
    global isUsualHit
    global isFuzzyHit

    res_points = points.get()
    res_points = int(res_points)

    res_velocity = velocity.get()
    res_velocity = int(res_velocity)

    defuzz = "Centroid"
    inference = "Max-Prod"

    if defuzzMethod.get() == "Метод центра тяжести":
        defuzz = "Centroid"
    if defuzzMethod.get() == "Метод правого максимума":
        defuzz = "Right-Max"
    if inferenceMethod.get() == "Метод максимума-минимума":
        inference = "Max-Min"
    if inferenceMethod.get() == "Метод максимума-произведения":
        inference = "Max-Prod"

    print(defuzzMethod.get())
    print(defuzzMethod.get())

    res_coeff = 3
    res_coeff = int(res_coeff)

    AircraftPoints = {"AircraftPoints": Plane,
                      "Missiles": {"Defuzzification": defuzz, "Direction": point2, "Inference": inference,
                                   "LaunchPoint": point1, "PropCoeff": res_coeff, "VelocityModule": res_velocity},
                      "StepsCount": res_points}

    ImitationRequest = json.dumps(AircraftPoints, ensure_ascii=False)
    import trajectory
    tr = trajectory.TrajectoryGenerator(ImitationRequest)
    ImitationResponse = tr.response_s
    data = json.loads(ImitationResponse)

    curvesBasicPoints = np.hstack(tuple(map(requestPointToNPPoint, data['AircraftTrajectory'])))
    for i in range(res_points - 5):
        x = curvesBasicPoints[0][i]
        y = curvesBasicPoints[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="BLACK", fill="BLACK")

    settings = data['UsualMissile']
    curvesUsual = np.hstack(tuple(map(requestPointToNPPoint, settings['Trajectory'])))
    UsualP = np.shape(curvesUsual)
    for i in range(UsualP[1] - 1):
        x = curvesUsual[0][i]
        y = curvesUsual[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="BLUE", fill="BLUE")
    UsualHit = settings['IsHit']

    settings = data['FuzzyMissile']
    curvesFuzzy = np.hstack(tuple(map(requestPointToNPPoint, settings['Trajectory'])))
    FuzzyP = np.shape(curvesFuzzy)
    for i in range(FuzzyP[1] - 1):
        x = curvesFuzzy[0][i]
        y = curvesFuzzy[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="RED", fill="RED")
    FuzzyHit = settings['IsHit']

    print("Usual missile hit?", UsualHit)
    print("Fuzzy missile hit?", FuzzyHit)

    if UsualHit:
        hitUsual.config(bg='green')
    else:
        hitUsual.config(bg='red')

    if FuzzyHit:
        hitFuzz.config(bg='green')
    else:
        hitFuzz.config(bg='red')

    oval1 = canvas.create_oval(0, 0, 0, 0, fill="YELLOW")
    oval2 = canvas.create_oval(0, 0, 0, 0, fill="PINK")
    oval3 = canvas.create_oval(0, 0, 0, 0, fill="ORANGE")
    # oval4 = canvas.create_oval(0, 0, 0, 0, outline= "GREEN", width=5)

    FuzzyFlag = False
    UsualFlag = False

    for i in range(res_points - 5):
        x1 = curvesBasicPoints[0][i]
        y1 = curvesBasicPoints[1][i]
        canvas.coords(oval1, x1 - 5.0, y1 + 5.0, x1 + 5.0, y1 - 5.0)
        time.sleep(0.02)
        window.update()

        if i < UsualP[1]:
            x2 = curvesUsual[0][i]
            y2 = curvesUsual[1][i]
            canvas.coords(oval2, x2 - 5.0, y2 + 5.0, x2 + 5.0, y2 - 5.0)
            window.update()

        if i < FuzzyP[1]:
            x3 = curvesFuzzy[0][i]
            y3 = curvesFuzzy[1][i]
            canvas.coords(oval3, x3 - 5.0, y3 + 5.0, x3 + 5.0, y3 - 5.0)
            window.update()

        if not FuzzyFlag:
            FuzzyFlag = i == FuzzyP[1]
            if FuzzyFlag:
                canvas.create_oval(x3 - 25.0, y3 + 25.0, x3 + 25.0, y3 - 25.0, outline="ORANGE", width=5)
        if not UsualFlag:
            UsualFlag = i == UsualP[1]
            if UsualFlag:
                canvas.create_oval(x2 - 25.0, y2 + 25.0, x2 + 25.0, y2 - 25.0, outline="ORANGE", width=5)

        if FuzzyFlag and UsualFlag:
            break


def rocket():
    def b1(event):
        global prev_x, prev_y
        global point1, point2
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        if prev_x:
            canvas.create_line(prev_x, prev_y, x, y, arrow=LAST)
            point1 = {"x": prev_x, "y": prev_y}
            point2 = {"x": x, "y": y}
            x = None
            y = None
        prev_x = x
        prev_y = y

    canvas.bind('<Button-1>', b1)


def plane():
    global Plane

    def b1(event):
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        canvas.create_oval(x - 5.0, y + 5.0, x + 5.0, y - 5.0, fill="BLACK")

        point = {"x": x, "y": y}
        Plane.append(point)

    canvas.bind('<Button-1>', b1)


def clean_canvas():
    canvas.delete("all")
    hitUsual.config(bg='red')
    hitFuzz.config(bg='red')
    Plane.clear()


scale = 1


def zoom_c(event):
    global scale
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    if event.num == 5 or event.delta == -120:
        canvas.scale('all', x, y, 0.9, 0.9)
    if event.num == 4 or event.delta == 120:
        canvas.scale('all', x, y, 1.1, 1.1)


if __name__ == "__main__":
    window = Tk()
    window.title("Имитатор наведения")
    sw = 1600  # window.winfo_screenwidth()
    sh = 900  # window.winfo_screenheight()
    window.geometry('%dx%d' % (sw - 300, sh - 300))

    f_right = Frame(window)
    f_right.pack(side=RIGHT)
    btn_st = Button(f_right, text="Simulate", command=start)
    btn_st.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + W + E)
    btn_clean = Button(f_right, text="Clear", command=clean_canvas)
    btn_clean.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + W + E)

    lbl_inferenceMethod = Label(f_right, text="Fuzzy")
    lbl_inferenceMethod.grid(column=0, row=1, padx=5, pady=5)
    inferenceMethod = Combobox(f_right, values=["Метод правого максимума", "Метод центра тяжести"], width=30)
    inferenceMethod.grid(column=1, row=1, padx=5, pady=5)
    inferenceMethod.current(1)

    lbl_defuzzMethod = Label(f_right, text="Defuzzy")
    lbl_defuzzMethod.grid(column=0, row=2, padx=5, pady=5)
    defuzzMethod = Combobox(f_right, values=["Метод максимума-минимума", "Метод максимума-произведения"], width=30)
    defuzzMethod.grid(column=1, row=2, padx=5, pady=5)
    defuzzMethod.current(1)

    imagerocket = PhotoImage(file="res/2.png")
    imageplane = PhotoImage(file="res/1.png")

    btn_rocket = Button(f_right, text="Наведение", command=rocket, image=imagerocket)
    btn_rocket.grid(column=0, row=3)

    btn_plane = Button(f_right, text="Траектория цели", command=plane, image=imageplane)
    btn_plane.grid(column=1, row=3)
    lbl_points = Label(f_right, text="Запас топлива")
    lbl_points.grid(column=0, row=4, padx=5, pady=5)
    points = Entry(f_right, width=10)
    points.grid(column=1, row=4, padx=5, pady=5)

    lbl_velocity = Label(f_right, text="Скорость сближения")
    lbl_velocity.grid(column=0, row=5, padx=5, pady=5)
    velocity = Entry(f_right, width=10)
    velocity.grid(column=1, row=5, padx=5, pady=5)

    # lbl_coeff = Label(f_left_middle, text="Коэфф проп-ти обычной ракеты")
    # lbl_coeff.grid(column=0, row=4)
    # coeff = Entry(f_left_middle, width=10)
    # coeff.grid(column=0, row=5)

    lbl_hitUsual = Label(f_right, text="Попадание ПМН")
    lbl_hitUsual.grid(column=0, row=6, padx=5, pady=5)
    hitUsual = Entry(f_right, width=5, bg='red')
    hitUsual.grid(column=1, row=6, padx=5, pady=5)

    lbl_hitFuzz = Label(f_right, text="Попадание НМН")
    lbl_hitFuzz.grid(column=0, row=7, padx=5, pady=5)
    hitFuzz = Entry(f_right, width=5, bg='red')
    hitFuzz.grid(column=1, row=7, padx=5, pady=5)

    canvas = Canvas(window, relief=RAISED, borderwidth=1, bg='WHITE', cursor="pencil")
    canvas.pack(side=RIGHT, padx=5)
    canvas.pack(fill=BOTH, expand=1)

    canvas.bind("<MouseWheel>", zoom_c)
    canvas.bind('<ButtonPress-3>', lambda event: canvas.scan_mark(event.x, event.y))
    canvas.bind("<B3-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

    # h = Scrollbar(window, orient=HORIZONTAL)
    # v = Scrollbar(window, orient=VERTICAL)
    # canvas = Canvas(window, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set, relief = RAISED, borderwidth=1, bg = 'WHITE', cursor = "pencil")
    # h['command'] = canvas.xview
    # v['command'] = canvas.yview
    # canvas.pack(side=RIGHT, padx=5)
    # canvas.pack(fill=BOTH, expand=1)

    st = Label(canvas, bg='WHITE')
    st.pack(side=TOP, expand=1)

    window.mainloop()
