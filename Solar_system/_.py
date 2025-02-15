import rebound
import math
from datetime import datetime, timedelta
class sollar_system:
    def __init__(self, ss):
        if ss:
            self.sim = rebound.Simulation()#'ss2.bin')
            self.sim.integrator = "mercurius"
            self.sim.add(["Sun", "Mercury","Venus","Earth","Mars", "Upiter", "Saturn", "Uran","Neptune"])
            #self.sim.save_to_file('ss.py')
            self.frequency = [9, 1, 4, 9, 16, 25*3, 36*4, 49*15, 64*15]
            self.frequency_copy = [9, 1, 4, 9, 16, 25 * 3, 36 * 4, 49 * 15, 64 * 15]
            self.c = [
                [[], (365-365//8)//self.frequency[3]],
                [[], (88-88//8)//self.frequency[1]],
                [[], (225-225//8)//self.frequency[2]],
                [[], (365-365//8)//self.frequency[3]],
                [[], (687-687//8)//self.frequency[4]],
                [[], (4332-4332//8)//self.frequency[5]],
                [[], (10759-10759//4)//self.frequency[6]],
                [[], (30660-30660//4)//self.frequency[7]],
                [[], (60190-60190//2)//self.frequency[8]]]
            self.trail_maker()
            self.createSolSys = 1
        else:
            self.sim = rebound.Simulation()
            self.sim.integrator = "mercurius"
            self.frequency = [9, 1, 4, 9, 16, 25 * 3, 36 * 4, 49 * 15, 64 * 15]
            self.frequency_copy = [9, 1, 4, 9, 16, 25 * 3, 36 * 4, 49 * 15, 64 * 15]
            self.c = []
            self.createSolSys = 0
        self.planets_A = {}
        self.q = -1
        self.integrator = 0
        self.data = 0
        self.sun_pos = 1

    def update(self):
        if self.sim.N > 0:
            self.sim.integrate(self.sim.t + self.integrator)

        if self.integrator > 0:
            self.data+=1
            self.q += 1
        elif self.integrator < 0:
            self.data -= 1
            self.q += 1
        pos = []
        _pos = []
        for i in range(self.sim.N):
            planet = self.sim.particles[i]
            _pos.append([planet.x, planet.y, planet.z])
            if i>len(self.c)-1:
                self.c.append([[], (365-365//8)//self.frequency[3]])
                self.frequency.append(9)
                self.frequency_copy.append(9)
            if self.sim.particles[0].x == 0 and self.sim.particles[0].y == 0 and self.sim.particles[0].z == 0:
                self.sun_pos = 0
            else:
                self.sun_pos = 1
            if i != 0 or self.sun_pos:
                if len(self.c[i][0]) < self.c[i][1]:
                    if self.q % self.frequency[i] == 0:
                        self.c[i][0].append([planet.x, planet.y, planet.z])
                else:
                    if self.planets_A != {}:
                        distance = 5
                        for _ in range(self.sim.N):
                            planet_B = self.sim.particles[_]
                            R = math.sqrt((planet.x - planet_B.x)**2 + (planet.y - planet_B.y)**2 + (planet.z - planet_B.z)**2)
                            if R > 0 and R < 0.5 and distance > 1:
                                distance = 1
                                self.frequency[i] = 1
                            elif R > 0.5 and R < 3 and distance > 2:
                                distance = 2
                                self.frequency[i] = 4
                            elif R > 3 and R < 6 and distance > 3:
                                distance = 3
                                self.frequency[i] = 9
                            elif self.frequency[i] != self.frequency_copy[i] and distance > 4:
                                distance = 4
                                self.frequency[i] = self.frequency_copy[i]

                    if self.q % self.frequency[i] == 0 and self.integrator != 0:
                        for _ in range(len(self.c[i][0]) - 1):
                            self.c[i][0][_] = self.c[i][0][_+1]
                    self.c[i][0][-1] = [planet.x, planet.y, planet.z]
        pos.append(_pos)
        pos.append(self.c)
        pos.append((datetime.now() + timedelta(days=self.data)).strftime("%d.%m.%Y"))
        pos.append(self.createSolSys)
        pos.append(self.planets_A)
        print(self.sim.N,pos)
        return pos
    def add(self, name, x, y, z, r, vx, vy, vz, m):
        self.sim.add(m=m, x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)
        self.planets_A[name] = [x, y, z, r, "textures/2k_mars.jpg"]

    def integration(self, i):
        self.integrator = i
    def trail_maker(self):
        for i in range(30095):
            self.sim.integrate(self.sim.t + -2 * math.pi / 361.156363004)

            for _ in range(1,9):
                if len(self.c[_][0]) < self.c[_][1] and i % self.frequency[_] == 0:
                    planet = self.sim.particles[_]
                    self.c[_][0].append([planet.x, planet.y, planet.z])
        self.sim.integrate(self.sim.t + (2 * math.pi / 361.156363004)*30095)
        for i in range(1,9):
            self.c[i][0] = self.c[i][0][::-1]
    def add_orbit(self):
        self.sim.add(
            m=1.0,  # масса планеты
            a=1.0,  # большая полуось
            e=0.5,  # эксцентриситет
            pomega=0.0,  # аргумент перицентра
            Omega=0.0,  # долгота восходящего узла
            inc=0.0,  # наклонение
            l=0.0  # долгота (положение вдоль орбиты)
        )
        planet = self.sim.particles[self.sim.N-1]
        self.planets_A["Viva cienta"] = [planet.x, planet.y, planet.z, 0.1, "textures/2k_mars.jpg"]

