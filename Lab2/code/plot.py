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

    if defuzzMethod.get() == "Центр тяжести":
        defuzz = "Centroid"
    if defuzzMethod.get() == "Пр. максимум":
        defuzz = "Right-Max"
    if inferenceMethod.get() == "Макс-мин":
        inference = "Max-Min"
    if inferenceMethod.get() == "Макс-произв":
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

    napr_p.delete(0, 'end')
    napr_p.insert(0, int(tr.p_angle[0]) )
    speed_p.delete(0, 'end')
    speed_p.insert(0, int(tr.p_vel[0]))
    pos_p.delete(0, 'end')
    pos_p.insert(0, "x:"+ str(int(tr.p_launch[0])) + " y:" + str(int(tr.p_launch[1])))

    napr_a.delete(0, 'end')
    napr_a.insert(0, int(tr.a_angle) )
    speed_a.delete(0, 'end')
    speed_a.insert(0, int(tr.a_vel))
    pos_a.delete(0, 'end')
    pos_a.insert(0, "x:"+ str(int(tr.a_launch[0])) + " y:" + str(int(tr.a_launch[1])))

    data = json.loads(ImitationResponse)

    curvesBasicPoints = np.hstack(tuple(map(requestPointToNPPoint, data['AircraftTrajectory'])))
    for i in range(res_points - 5):
        x = curvesBasicPoints[0][i]
        y = curvesBasicPoints[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="#343434", fill="#343434")

    settings = data['UsualMissile']
    curvesUsual = np.hstack(tuple(map(requestPointToNPPoint, settings['Trajectory'])))
    UsualP = np.shape(curvesUsual)
    for i in range(UsualP[1] - 1):
        x = curvesUsual[0][i]
        y = curvesUsual[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="#ea411c", fill="#ea411c")
    UsualHit = settings['IsHit']

    settings = data['FuzzyMissile']
    curvesFuzzy = np.hstack(tuple(map(requestPointToNPPoint, settings['Trajectory'])))
    FuzzyP = np.shape(curvesFuzzy)
    for i in range(FuzzyP[1] - 1):
        x = curvesFuzzy[0][i]
        y = curvesFuzzy[1][i]
        if i % 3 == 0:
            canvas.create_oval(x - 2.0, y + 2.0, x + 2.0, y - 2.0, outline="#3da927", fill="#3da927")
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
            canvas.create_line(prev_x, prev_y, x, y, arrow=LAST, dash=1, fill="grey", smooth=True)
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
        canvas.create_oval(x - 3.0, y + 3.0, x + 3.0, y - 3.0, fill="#5a5a5a")

        point = {"x": x, "y": y}
        Plane.append(point)

    canvas.bind('<Button-1>', b1)


def clean_canvas():
    canvas.delete("all")
    hitUsual.config(bg='red')
    hitFuzz.config(bg='red')
    Plane.clear()
    napr_p.delete(0, 'end')
    speed_p.delete(0, 'end')
    pos_p.delete(0, 'end')
    napr_a.delete(0, 'end')
    speed_a.delete(0, 'end')
    pos_a.delete(0, 'end')



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
    imagerocket = PhotoImage(file="res/missile.png")
    imageplane = PhotoImage(file="res/plane.png")
    imagestart = PhotoImage(file="res/start.png")
    imageclear = PhotoImage(file="res/clear.png")

    btn_st = Button(f_right, image=imagestart, command=start)
    btn_st.grid(row=0, column=0, pady=5)
    btn_clean = Button(f_right, image=imageclear, command=clean_canvas)
    btn_clean.grid(row=1, column=0, pady=5)

    # lbl_inferenceMethod = Label(f_right, text="Fuzzy")
    # lbl_inferenceMethod.grid(column=0, row=1)

    btn_rocket = Button(f_right, text="Наведение", command=rocket, image=imagerocket)
    btn_rocket.grid(column=0, row=3, pady=5)

    btn_plane = Button(f_right, text="Траектория цели", command=plane, image=imageplane)
    btn_plane.grid(column=0, row=4, pady=5)

    inferenceMethod = Combobox(f_right, values=["Пр. максимум", "Центр тяжести"], width="13", state="readonly")
    inferenceMethod.grid(column=0, row=5, pady=5)
    inferenceMethod.current(1)

    # lbl_defuzzMethod = Label(f_right, text="Defuzzy")
    # lbl_defuzzMethod.grid(column=0, row=2)
    defuzzMethod = Combobox(f_right, values=["Макс-мин", "Макс-произв"], width="13", state="readonly")
    defuzzMethod.grid(column=0, row=6, pady=5)
    defuzzMethod.current(1)

    lbl_points = Label(f_right, text="Длина тр.")
    lbl_points.grid(column=0, row=7, pady=5)
    points = Entry(f_right, width=10)
    points.insert(0, 300)
    points.grid(column=0, row=8, pady=5)

    lbl_velocity = Label(f_right, text="Скор. пер.")
    lbl_velocity.grid(column=0, row=9, pady=5)
    velocity = Entry(f_right, width=10)
    velocity.insert(0, 7)
    velocity.grid(column=0, row=10, pady=5)

    # lbl_coeff = Label(f_left_middle, text="Коэфф проп-ти обычной ракеты")
    # lbl_coeff.grid(column=0, row=4)
    # coeff = Entry(f_left_middle, width=10)
    # coeff.grid(column=0, row=5)

    lbl_hitUsual = Label(f_right, text="ПМН", fg="#ea411c")
    lbl_hitUsual.grid(column=0, row=11, pady=5)
    hitUsual = Entry(f_right, width=5, bg='red')
    hitUsual.grid(column=0, row=12, pady=5)

    lbl_hitFuzz = Label(f_right, text="НМН", fg = "#3da927")
    lbl_hitFuzz.grid(column=0, row=13, pady=5)
    hitFuzz = Entry(f_right, width=5, bg='red')
    hitFuzz.grid(column=0, row=14, pady=5)

    canvas = Canvas(window, relief=RAISED, borderwidth=1, bg='WHITE', cursor="pencil")
    canvas.pack(side=TOP,anchor=NW, padx=5)
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
    f_down = Frame(window)
    f_down.pack(side=BOTTOM,anchor=SW, padx=5)
    lbl_pos_p = Label(f_down, text="Пол. пер.")
    lbl_pos_p.grid(column=0, row=0 )
    pos_p = Entry(f_down, width=10)
    pos_p.grid(column=1, row=0)
    lbl_napr_p = Label(f_down, text="Напр. пер.")
    lbl_napr_p.grid(column=3, row=0 )
    napr_p = Entry(f_down, width=10)
    napr_p.grid(column=4, row=0)
    lbl_speed_p = Label(f_down, text="Скор. пер.")
    lbl_speed_p.grid(column=5, row=0 )
    speed_p = Entry(f_down, width=10)
    speed_p.grid(column=6, row=0)


    lbl_pos_a = Label(f_down, text="Пол. цели.")
    lbl_pos_a.grid(column=7, row=0 )
    pos_a = Entry(f_down, width=10)
    pos_a.grid(column=8, row=0)
    lbl_napr_a = Label(f_down, text="Напр. цели.")
    lbl_napr_a.grid(column=9, row=0 )
    napr_a = Entry(f_down, width=10)
    napr_a.grid(column=10, row=0)
    lbl_speed_a = Label(f_down, text="Скор. цели.")
    lbl_speed_a.grid(column=11, row=0 )
    speed_a = Entry(f_down, width=10)
    speed_a.grid(column=12, row=0)

    st = Label(canvas, bg='WHITE')
    st.pack(side=TOP, expand=1)

    window.mainloop()
