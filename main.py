from tkinter import *
import time


class Physics:
    radius_to_mass_const = 4
    free_value = 2
    current_res = 1

    def __init__(self, accel, speed, mass, pos, is_movable, color):
        self.accel = accel
        self.speed = speed
        self.mass = mass
        self.pos = pos
        self.is_movable = is_movable
        self.color = color

    def set_pos(self, pos):
        self.pos = pos

    def set_accel(self, accel):
        self.accel = accel

    def set_speed(self, speed):
        self.speed = speed

    def set_mass(self, mass):
        self.mass = mass

    def set_is_movable(self, is_movable):
        self.is_movable = is_movable

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.pos

    def get_accel(self):
        return self.accel

    def get_speed(self):
        return self.speed

    def get_mass(self):
        return self.mass

    def get_is_movable(self):
        return self.is_movable

    def get_radius(self):
        radius = Physics.radius_to_mass_const * pow(self.mass, 0.33) / Physics.current_res + self.free_value
        return radius

    def get_color(self):
        return self.color


def update_accel(elem):
    sumaccel = elem.get_accel()
    diminished_planets.remove(elem)
    for other_planet in diminished_planets:
        pos1 = elem.get_pos()
        x1 = pos1[0]
        y1 = pos1[1]
        pos2 = other_planet.get_pos()
        x2 = pos2[0]
        y2 = pos2[1]
        xdist = x2 - x1
        ydist = y2 - y1
        if xdist != 0 and ydist != 0:
            m1 = elem.get_mass()
            m2 = other_planet.get_mass()
            distancesquared = xdist * xdist + ydist * ydist
            distance = pow(distancesquared,0.5)
            force = gravity_constant / distancesquared/distance
            accel_orig = force*m2
            accel_other = force*m1
            sumaccel[0] += accel_orig*xdist
            sumaccel[1] += accel_orig*ydist
            other_accel = other_planet.get_accel()
            other_accel[0] -= accel_other*xdist
            other_accel[1] -= accel_other*ydist
            other_planet.set_accel(other_accel)
    elem.set_accel(sumaccel)


def draw():
    a.delete("all")
    for elem in allplanets:
        cpos = elem.get_pos()
        pos = [0, 0]
        pos[0] = (cpos[0] - camera_pos["x"]) / Physics.current_res + half_width
        x2 = (pos[0] + elem.get_radius())
        if x2 > 0:
                x1 = (pos[0] - elem.get_radius())
                if x1 < real_width:
                    pos[1] = (cpos[1] - camera_pos["y"]) / Physics.current_res + half_height
                    y2 = (pos[1] + elem.get_radius())
                    if y2 > 0:
                        y1 = (pos[1] - elem.get_radius())
                        if y1 < real_height:
                            a.create_oval(x1, y1, x2, y2, fill=elem.get_color())
    if pointer_set["is_on_screen"]:
        screen_x = (pointer_set["x"] - camera_pos["x"]) / Physics.current_res + half_width
        screen_y = (pointer_set["y"] - camera_pos["y"]) / Physics.current_res + half_height
        pointersize = pointer_set["pointer_size"] / Physics.current_res + Physics.free_value
        a.create_oval(screen_x - pointersize, screen_y - pointersize, screen_x + pointersize,
                      screen_y + pointersize, fill="white", tag="pointer")

def save_situation():
    global allplanets
    if allplanets != []:
        f = open("saved_planets.txt", 'a')
        f.write('[')
        iterations = len(allplanets)
        i = 0
        while i < iterations:
            f.write(
                f'Physics({allplanets[i].get_accel()}, {allplanets[i].get_speed()}, {allplanets[i].get_mass()}, {allplanets[i].get_pos()}, {allplanets[i].get_is_movable()}, "{allplanets[i].get_color()}")')
            if i + 1 < iterations:
                f.write(", ")
            else:
                f.write("]\n")
            i += 1
        f.close()


def main_cycle():
    global Next_wanted_time, wait_time, diminished_planets
    diminished_planets = []
    draw_time = int(Time_for_frame / 7 + 0.00006*len(allplanets)*1000)
    if physics_is_applied:

        current_time = time.time()
        if current_time > Next_wanted_time:
            diminished_planets = allplanets.copy()
            for planet in allplanets:
                planet.set_accel([0,0])
            for planet in allplanets:
                update_accel(planet)
            for elem in allplanets:
                if elem.get_is_movable():
                    a = elem.get_accel()
                    c = elem.get_speed()
                    c = [c[0] + a[0], c[1] + a[1]]
                    elem.set_speed(c)
                    v = elem.get_pos()
                    elem.set_pos([c[0] + v[0], c[1] + v[1]])
            Next_wanted_time += Time_for_frame
            scene.after(draw_time, lambda: [main_cycle()])
        else:

            scene.after(int(Time_for_frame / 8 * 1000), lambda: [main_cycle()])
        draw()


def coords_of_click(event):
    if event.y > 55:
        global pointer_set, choiceinprogress
        for child in a.winfo_children():
            child.destroy()
        choiceinprogress = True
        pointer_set["is_on_screen"] = True
        pause_simulation()
        real_y = (event.y - half_height) * Physics.current_res + camera_pos["y"]
        real_x = (event.x - half_width) * Physics.current_res + camera_pos["x"]
        pointer_set["x"] = real_x
        pointer_set["y"] = real_y
        create_planet_UI["speedxlabel"].place(x=350, y=24)
        create_planet_UI["speedylabel"].place(x=450, y=24)
        create_planet_UI["masslabel"].place(x=550, y=24)
        create_planet_UI["ismovablelabel"].place(x=650, y=24)
        create_planet_UI["colorlabel"].place(x=750, y=24)
        create_planet_UI['speedentryx'].place(x=350, y=4)
        create_planet_UI['speedentryy'].place(x=450, y=4)
        create_planet_UI['massentry'].place(x=550, y=4)
        create_planet_UI['ismovableentry'].place(x=650, y=4)
        create_planet_UI["colorentry"].place(x=750, y=4)
        create_planet_UI['applybutton'].place(x=850, y=4)
        draw()


def apply_planet():
    global choiceinprogress
    planet = Physics([0, 0], [0, 0], 20
                     , [pointer_set['x'], pointer_set['y']], 1, "#FFFFFF")
    try:
        if create_planet_UI['speedentryx'].get() != "":
            planet.set_speed([float(create_planet_UI['speedentryx'].get()), planet.get_speed()[1]])
    except ValueError:
        create_planet_UI['speedentryx'].delete(0, END)
    try:
        if create_planet_UI['speedentryy'].get() != "":
            planet.set_speed([planet.get_speed()[0], float(create_planet_UI['speedentryy'].get())])
    except ValueError:
        create_planet_UI['speedentryy'].delete(0, END)
    try:
        if create_planet_UI['massentry'].get() != "":
            planet.set_mass(float(create_planet_UI['massentry'].get()))
    except ValueError:
        create_planet_UI['massentry'].delete(0, END)
    try:
        if create_planet_UI['ismovableentry'].get() != "":
            if int(create_planet_UI['ismovableentry'].get()) == 0 or int(create_planet_UI['ismovableentry'].get()) == 1:
                planet.set_is_movable(int(create_planet_UI['ismovableentry'].get()))
    except ValueError:
        create_planet_UI['ismovableentry'].delete(0, END)

    if len(create_planet_UI['colorentry'].get()) == 7 and create_planet_UI['colorentry'].get()[0] == "#":
        isacolor=True
        for symbol in create_planet_UI['colorentry'].get()[1:]:
            if symbol not in "ABCDEFabcdef1234567890":
                isacolor=False
        if isacolor:
            planet.set_color(create_planet_UI['colorentry'].get())
        else:
            create_planet_UI['colorentry'].delete(0, END)
    else:
        create_planet_UI['colorentry'].delete(0, END)
    allplanets.append(planet)
    deleteUI()
    pointer_set["is_on_screen"] = False
    print(len(allplanets))
    draw()


def zoomer(event):
    global physics_is_applied
    if event.delta > 0:
        Physics.current_res += (0.1 * Physics.current_res)
    else:
        Physics.current_res -= (0.1 * Physics.current_res)
    draw()





def deleteUI():
    global choiceinprogress
    choiceinprogress = False
    for thingie in create_planet_UI:
        create_planet_UI[f'{thingie}'].place_forget()


def restart_field():
    global allplanets, pointer_set, Time_for_frame_mod
    camera_pos["x"] = half_width
    camera_pos["y"] = half_height
    pointer_set["is_on_screen"] = False
    allplanets = []
    deleteUI()
    for thing in a.winfo_children():
        thing.destroy()
    pause_simulation()
    Physics.current_res = 1
    Time_for_frame_mod = Time_for_frame
    draw()


if __name__ == '__main__':

    scene = Tk()
    scene.resizable(False, False)
    real_width = scene.winfo_screenwidth() - 10
    real_height = scene.winfo_screenheight() - 30
    half_height = real_height/2
    half_width = real_width/2
    scene.geometry(f'{real_width}x{real_height}')
    scene.title("Newly optimized")
    a = Canvas(scene, bg="#000000", height=real_height, width=real_width)
    camera_pos = {"x": half_width, "y": half_height}
    gravity_constant = 10
    choiceinprogress = False
    pointer_set = {"x": 0.0, "y": 0.0, "is_on_screen": False, "pointer_size": 5}
    create_planet_UI = {"speedentryx": Entry(scene, fg="#FFFFFF", background="#000000"),
                        "speedentryy": Entry(scene, fg="#FFFFFF", background="#000000"),
                        "massentry": Entry(scene, fg="#FFFFFF", background="#000000"),
                        "ismovableentry": Entry(scene, fg="#FFFFFF", background="#000000"),
                        "colorentry": Entry(scene, fg="#FFFFFF", background="#000000"),
                        "ismovablelabel": Label(scene, fg="#FFFFFF", background="#000000", text="Dynamic/static"),
                        "speedxlabel": Label(scene, fg="#FFFFFF", background="#000000", text="Horizontal speed"),
                        "speedylabel": Label(scene, fg="#FFFFFF", background="#000000", text="Vertical speed"),
                        "masslabel": Label(scene, fg="#FFFFFF", background="#000000", text="Mass"),
                        "colorlabel": Label(scene, fg="#FFFFFF", background="#000000", text="Color"),
                        "applybutton": Button(scene, text="Apply", bg="#000000", fg="#ffffff", font=("Courier", 12),
                                              command=lambda: [apply_planet()], bd=1,
                                              width=10)
                        }
    Time_for_frame = 0.03
    wait_time = int(Time_for_frame / 8 * 1000)
    Next_wanted_time = time.time()
    physics_is_applied = 0  # 0 means no physics
    horizontalscrollspeed = 40
    verticalscrollspeed = 30

    a.pack()
    scene.bind("<MouseWheel>", zoomer)
    allplanets=[]
    allplanets = [Physics([0, 0], [-0.01, 0.08], 500, [real_width / 2, real_height / 2], 1, "#FFFF1F"),
                  Physics([0, 0], [0, -2.9024891309012275097956013], 0.01, [real_width / 2 + 285.2, real_height / 2], 1,
                          "#FF1F1F"),
                  Physics([0, 0], [0, -4], 10, [real_width / 2 + 340, real_height / 2], 1, "#a1a1FF")]
   # i = 1
   #while i < 300:
   #     allplanets.append(Physics([0, 0], [-0, 0], i, [i*2, 12*i-13], 1, "#FFFF1F"))
   #     i += 1


    def start_simulation():
        global physics_is_applied, pointer_set, Next_wanted_time, Time_for_frame
        deleteUI()
        for thing in a.winfo_children():
            thing.destroy()
        if not physics_is_applied:
            physics_is_applied = 1
            Next_wanted_time = time.time() + Time_for_frame
        pointer_set["is_on_screen"] = False
        draw()
        main_cycle()


    def leftKey(event):
        camera_pos["x"] -= Physics.current_res * horizontalscrollspeed
        draw()


    def rightKey(event):
        camera_pos["x"] += Physics.current_res * horizontalscrollspeed
        draw()


    def downKey(event):
        camera_pos["y"] += Physics.current_res * (verticalscrollspeed)
        draw()


    def upKey(event):
        camera_pos["y"] -= Physics.current_res * (verticalscrollspeed)
        draw()


    def pause_simulation():
        global physics_is_applied
        if physics_is_applied:
            physics_is_applied = 0


    def center_field():
        camera_pos['x'] = half_width
        camera_pos['y'] = half_height
        Physics.current_res = 1
        draw()


    def space_decision(event):
        if physics_is_applied:
            pause_simulation()
        else:
            start_simulation()


    def enter_logic(event):
        if choiceinprogress:
            apply_planet()


    save_button = Button(scene, text="Save", bg="#000000", fg="#ffffff", font=("Courier", 20), command=save_situation,
                         bd=1,
                         width=5).place(x=real_width - 100, y=5)
    unpause_button = Button(scene, text="Unpause", bg="#000000", fg="#ffffff", font=("Courier", 20),
                            command=lambda: [start_simulation()], bd=1,
                            width=10)
    unpause_button.place(x=4, y=5)
    pause_button = Button(scene, text="Pause", bg="#000000", fg="#ffffff", font=("Courier", 20),
                          command=lambda: [pause_simulation()], bd=1,
                          width=10)
    restart_button = Button(scene, text="Clear", bg="#000000", fg="#ffffff", font=("Courier", 20),
                            command=lambda: [restart_field()], bd=1,
                            width=10)
    return_button = Button(scene, text="Center", bg="#000000", fg="#ffffff", font=("Courier", 20),
                           command=lambda: [center_field()], bd=1,
                           width=10)
    return_button.place(x=real_width - 440, y=5)
    pause_button.place(x=164, y=5)
    restart_button.place(x=real_width - 270, y=5)
    scene.bind("<1>", coords_of_click)
    scene.bind('<Left>', leftKey)
    scene.bind('<Right>', rightKey)
    scene.bind('<Up>', upKey)
    scene.bind('<Down>', downKey)
    scene.bind('<space>', space_decision)
    scene.bind('<Return>', enter_logic)
    draw()
    main_cycle()
    scene.mainloop()
