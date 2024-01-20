import pandas as pd
import matplotlib.pyplot as plt
import simpy
import random
import names

#simulating driver data
#1 time unit = 1 min
#things to consider:
#stop lights - currently have "crosswalks", how do we consider stoplights?
#speed limits - how to consider speed limits? split up the route into different parts then combining the data?
#picking the best driver?

class Route:
    #distance - set distance in km
    #recommended_speed - in km/h
    #maxstop - max # of stops
    #deltat - time increment in minutes
    def __init__(self, route_name, distance, recommended_speed, maxstop, deltat):
        self.route_name = route_name
        self.distance = distance
        self.recommended_speed = recommended_speed
        self.maxstop = maxstop
        self.deltat = deltat
        
class Driver:
    #drivers - number of drivers
    #inc - speed increment in km/h
    drivers = 0
    inc = 0
    all_velocities = []
    all_times = []
    all_pwr_exp = []
    all_safe_time = []
    all_behaviour_scores = []
    all_eps = []
    all_enjoyment_score = []
    
    def __init__(self, env, route, inc):
        #driverID - driver number
        #driver_stats - array containing name, avg velocity, time elapsed, power expenditure, % of time following
        #recommended speed (safe time), behaviour score, emergency preparedness score, enjoyment score
        #name - randomly generated name
        #mass - weight of person, in kg
        #eps - emergency preparedness score from 1 to 5
        #enjoy - enjoyment score from 1 to 5
        #distance_left - distance left to travel in km
        self.env = env
        self.driverID = self.drivers
        self.driver_stats = []
        self.name = names.get_first_name()
        self.mass = random.randint(40,100)
        self.eps = random.randint(1,5)
        self.enjoy = random.randint(1,5)
        self.distance_left = route.distance
        Driver.inc = inc

        #powerexp - power expenditure calculated by kinetic energy/time in Watts
        #time_elapsed - time it took to complete route in minutes
        #current_speed - keep track of current speed in km/h
        #avg_speed - average speed over time in km/h
        #behaviour_score - "Safe" >= 70%, "Moderate" >= 50%, "Reckless" < 50%
        #safetime - % time at recommended speed
        #stops - number of stops made
        self.power_exp = 0
        self.time_elapsed = 0
        self.current_speed = 0
        self.avg_speed = 0
        self.behaviour_score = 0
        self.safetime = 0
        self.stops = 0

        #speeds - for calculating safe time
        self.speeds = []
        self.speedtimes = []
    
    def update_values(self, route, time_elapsed):
        self.time_elapsed = time_elapsed
        #km/(min/60 -> hours)
        self.avg_speed = route.distance/(self.time_elapsed/60)
        #car weighs ~1000kg
        #power exp per hour
        self.power_exp = 0.5*(self.mass + 1000)*pow(self.avg_speed/3.6,2)/(self.time_elapsed*60)

        #calculate percentage of time within recommended speed (can be changed)
        sum_safe = 0
        for i in range (-2,2):
            sum_safe += self.speeds.count(route.recommended_speed+i*Driver.inc)
        self.safetime = min(100,round(sum_safe/len(self.speeds),4) * 100)

        #calculate behaviour score (can be changed)
        if (self.safetime > 50):
            if (self.safetime >= 70):
                self.behaviour_score = "Safe"
            else:
                self.behaviour_score = "Moderate"
        else: self.behaviour_score = "Reckless"
        
        self.driver_stats = [self.name, round(self.avg_speed,2), round(self.time_elapsed,2), round(self.power_exp,2),
                             round(self.safetime,2), self.behaviour_score, self.eps, self.enjoy]

        Driver.all_velocities.append(self.driver_stats[1])
        Driver.all_times.append(self.driver_stats[2])
        Driver.all_pwr_exp.append(self.driver_stats[3])
        Driver.all_safe_time.append(self.driver_stats[4])
        Driver.all_behaviour_scores.append(self.driver_stats[5])
        Driver.all_eps.append(self.driver_stats[6])
        Driver.all_enjoyment_score.append(self.driver_stats[7])
        return self.driver_stats

    def start_car(self, env, route):
        #start car
        v0 = 0
        v1 = route.recommended_speed/3.6
        #2.0m/s^2 - average car acceleration
        a = 2.0
        t = (v1-v0)/a
        d = (pow(v1,2)-pow(v0,2))/(2*a)
        self.current_speed = route.recommended_speed
        self.speeds.append((d/t)*3.6)
        self.distance_left -= d/1000
        
        yield self.env.timeout(t/60)
        
    def stop_car(self, env, route):
        #stop car
        v0 = self.current_speed/3.6
        v1 = 0
        #2.0m/s^2 - average car acceleration
        a = -2.0
        t = (v1-v0)/a
        d = (pow(v1,2)-pow(v0,2))/(2*a)
        self.current_speed = 0
        self.speeds.append((d/t)*3.6)
        self.distance_left -= d/1000
        
        yield self.env.timeout(t/60)
        
    
    def move(self, route):
        x = random.uniform(0,1)
        #40% chance to speed up
        if (x >= 0.7):
            if (self.current_speed < route.recommended_speed + self.inc*5):
                self.current_speed += self.inc
        #20% to slow down
        elif (x <= 0.3):
            if (self.current_speed > route.recommended_speed - self.inc*2):
                    self.current_speed -= self.inc
        #distance remaining calculation
        self.distance_left -= (self.current_speed/60)*route.deltat
        #keep track of speed based on the set interval
        self.speeds.append(self.current_speed)
        yield self.env.timeout(route.deltat)

def drive_route(env, driver, route):
    start_time = env.now

    #actually driving
    while (driver.distance_left > 0):
        #accelerating from stop
        if (driver.current_speed == 0):
            yield env.process(driver.start_car(env, route))
            #self.speedtime(env.now-start_time)
        #drive car
        else:
            yield env.process(driver.move(route))
            #chance of stopping at crosswalks 50%
            if (driver.stops < route.maxstop):
                if (random.choice([True, False])):
                    yield env.process(driver.stop_car(env, route))
                    #let the people cross the street
                    yield env.timeout(random.randint(3,15)/60)
                    yield env.process(driver.start_car(env, route))
                    driver.stops += 1

    #time spent
    time_elapsed = env.now-start_time
    #calculate driver stats
    driver.update_values(route, time_elapsed)
    
def sim_drivers(env, route, num_drivers):
    driver_instances =[]
    for i in range (num_drivers):
        d = Driver(env, route, 3)
        env.process(drive_route(env, d, route))
        driver_instances.append(d)
    return driver_instances
    

def get_route():

    route_name = "Ring Road"
    distance = 2.5
    recommended_speed = 35
    maxstop = 4
    deltat = 3/60
    num_drivers = 30
    '''
    route_name = input("Input route name: ")
    distance = float(input("Input route length in km: "))
    recommended_speed = int(input("Input recommended speed in km/h: "))
    maxstop = int(input("Input # of crosswalks: "))
    deltat = float(input("Input time between speed updates in minutes: "))
    num_drivers = int(input("Input number of drivers to simulate: "))
    '''
    params = [route_name, distance, recommended_speed, maxstop, deltat, num_drivers]
    return params

def plot_avg_velocity_vs_time():
    plt.figure(1)
    plt.scatter(Driver.all_times, Driver.all_velocities)
    plt.xlabel('Total time (min)')
    plt.ylabel('Average Velocity (km/h)')
    plt.title('Average Velocity vs Time')

def plot_behaviour_score():
    plt.figure(2)
    categories = ["Reckless", "Moderate", "Safe"]
    values = [Driver.all_behaviour_scores.count("Reckless"), Driver.all_behaviour_scores.count("Moderate"), Driver.all_behaviour_scores.count("Safe")]
    plt.bar(categories, values)
    plt.title("Driver Behaviour Scores")
    
def main():
    #gets the same data every time
    #can delete to randomize
    random.seed(100)
    #take in route variables
    route_name, distance, recommended_speed, maxstop, deltat, num_drivers = get_route()
    route = Route(route_name, distance, recommended_speed, maxstop, deltat)

    env = simpy.Environment()
    #contains all the drivers
    driver_instances = sim_drivers(env,route,num_drivers)
    env.run()

    #all the different stats
    headings = ["Names", "Average Velocity (km/h)", "Total Time Elapsed (min)", "Power Expenditure (W)",
            "Percentage of time following recommended speed", "Behaviour Score", "Emergency Preparedness Score",
            "Enjoyment Score"]
    
    data = [driver.driver_stats for driver in driver_instances]
    df = pd.DataFrame(data, columns=headings)
    df.to_csv(f"{route_name} Drivers.csv", index=False)

    plot_avg_velocity_vs_time()
    plot_behaviour_score()
    plt.show()
    
if __name__ == "__main__":
    main()
