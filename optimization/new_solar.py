from math import cos, sin, pi, acos, tan, asin
from numpy import linspace

from math import pi
import csv
import os

def to_rad(angle):
    rad = angle * 2 * pi / 360
    return rad


def integrate(x, y):
    # Given an X and Y data set, numerically integrate
    integral = 0
    for i in range(len(x) - 1):
        integral += (x[i + 1] - x[i]) * (y[i + 1] + y[i]) / 2
    return integral

class SolarDay:

    def __init__(self, day, latitude, longitude,
                 timezone, cloudiness, module_angle):
        self.day = day
        self.lat = latitude
        self.long = longitude
        # Cloudiness is the percentage of solar insolation
        # Not being blocked by clouds (i.e. between 0 and 1)
        self.cloud = cloudiness
        # Given as an integer of the difference between us and UTC
        self.points = []
        self.time = timezone
        # the module angle is the panel angle wrt the horizontal plane.
        # 0 degrees/rad faces North (front of car)
        self.mod_angle = module_angle

    def declination_angle(self):
        # Declination angle is the angle the sun sits in the sky at noon
        d = -23.45 * cos(to_rad(360 / 365) * (self.day + 10))
        return d
        
    def time_correction(self):
        # Measurement of the difference in angle between us and UTC
        LSTM = 15 * self.time
        B = 360/365 * self.day * -81
        EoT = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B)
        TC = 4 * (self.long - LSTM) + EoT
        return TC
    
    def AM(self, HRA):
        elevation = (asin(sin(to_rad(self.declination_angle()))
                     * sin(to_rad(self.lat))
                     + cos(to_rad(self.declination_angle()))
                     * cos(to_rad(self.lat)) * cos(HRA)))
        zenith = (pi / 2) - elevation
        AM = 1 / cos(zenith)
        return AM

    def solar_insolation(self, HRA):
        # gives value in kW/m^2
        ID = 1.353 * 0.7 ** (self.AM(HRA) ** 0.678)  # Incident radiation
        elevation = to_rad(90 - self.lat + self.declination_angle())
        IM = ID * sin(to_rad(self.mod_angle) + elevation)
        return IM

    # HRA is the solar time at the car location
    def time_to_HRA(self, time):
        LST = time + self.time_correction() / 60
        HRA = to_rad(15) * (LST - 12)
        return HRA

    def energy_received(self):
        points = linspace(self.sunrise(),
                          self.sunset(), 1000, endpoint=False).tolist()
        energy = []
        for i in range(len(points)):
            energy.append(self.solar_insolation(self.time_to_HRA(points[i])))
        self.total_energy = integrate(points, energy) * self.cloud
        return(energy, points)

class SolarArray:
    def data(self):
        array = []
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                cell = {"Cell_ID": row[0], "Angle": row[4]}
                array.append(cell)
        # print(array)
        return(array)

    # calculate and store total energy values
    def totalEnergy(self):
        total_energy = 0
        array = self.data()
        for i in range(1, len(self.data())):
            module_angle = float(array[i]['Angle'])
            d = SolarDay(self.day, self.lat, self.long,
                         self.time, self.cloud, module_angle)
            insol = integrate(d.energy_received()[1], d.energy_received()[0])
            energy = insol * 5 * 0.17
            total_energy = total_energy + energy

        return(total_energy)

if __name__ == '__main__':
    test = SolarArray(182, 30.28, 97.73, 8, 0.5)
    print(test.totalEnergy())
