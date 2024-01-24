from turtle import Shape, Screen, Turtle, Vec2D as Vec

G = 8
NUM_LOOPS = 4100
Ro_X = 0
Ro_Y = -85
Vo_X = 485
Vo_Y = 0

class GravSys():
    def __init__(self):
        self.bodies = [] #CSM 객체들을 저장할 bodies라는 빈 리스트를 만든다. 
        self.t = 0
        self.dt = 0.001
    
    def sim_loop(self):
        for _ in range(NUM_LOOPS):
            self.t += self.dt
            for body in self.bodies:
                body.step()# 시간 단계를 제어한다. 

class Body(Turtle):
    def __init__(self, mass, start_loc, vel, gravsys, shape):
        super().__init__(shape=shape)
        self.gravsys = gravsys
        self.penup()
        self.mass = mass 
        self.setpos(start_loc)
        self.vel = vel
        gravsys.bodies.append(self)
        #self.resizemode("user")
        #self.pendown()

    def acc(self):
        a = Vec(0, 0)
        for body in self.gravsys.bodies:
            if body != self:
                r = body.pos() - self.pos()
                a += (G*body.mass/ abs(r)**3) * r # 중력가속도 법칙
        return a

    def step(self):
        dt = self.gravsys.dt
        a = self.acc()
        self.vel = self.vel + dt*a
        self.setpos(self.pos() + dt*self.vel)
        if self.gravsys.bodies.index(self) == 2:
            rotate_factor = 0.0006
            self.setheading((self.heading()-rotate_factor*self.xcor()))
            if self.xcor() < -20:
                self.shape('arrow')
                self.shapesize(0.5)
                self.setheading(105)

def main():
    screen = Screen()
    screen.setup(width=1.0, height=1.0)
    screen.bgcolor('black')
    screen.title("Apollo 8 Free Return Simulation")
    gravsys = GravSys()

    image_earth = 'earth_100x100.gif'
    screen.register_shape(image_earth)
    earth = Body(1000000, (0,-25), Vec(0, -2.5), gravsys, image_earth)
    earth.pencolor('white')
    earth.getscreen().tracer(n=0, delay=0)
    image_moon = 'moon_27x27.gif'
    screen.register_shape(image_moon)
    moon = Body(32000, (344,42), Vec(-27,147), gravsys, image_moon)
    moon.pencolor('gray')

    csm = Shape('compound')
    cm = ((0,30),(0,-30),(30,0))
    csm.addcomponent(cm, 'white', 'white')
    sm = ((-60,30),(0,30),(0,-30),(-60,-30))
    csm.addcomponent(sm, 'white', 'black')
    nozzle = ((-55,0),(-90,20),(-90,-20))
    csm.addcomponent(nozzle, 'white', 'white')
    screen.register_shape('csm',csm)

    ship = Body(1, (Ro_X, Ro_Y), Vec(Vo_X, Vo_Y), gravsys, 'csm')
    ship.shapesize(0.2)
    ship.color('white')
    ship.getscreen().tracer(1.0)
    ship.setheading(90)
    gravsys.sim_loop()

if __name__ == '__main__':
    main()
                   