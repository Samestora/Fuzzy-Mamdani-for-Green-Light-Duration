import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from flask import Flask, render_template, jsonify, request

# IF-THEN
bike_count = ctrl.Antecedent(np.arange(0, 31, 1), 'bike_count')
car_count = ctrl.Antecedent(np.arange(0, 21, 1), 'car_count')
road_width = ctrl.Antecedent(np.arange(2, 11, 1), 'road_width')
green_light = ctrl.Consequent(np.arange(5, 36, 1), 'green_light')


# for bikes
# DATA : Observation

bike_count['low'] = fuzz.trapmf(bike_count.universe, [0, 0, 7, 15])
bike_count['medium'] = fuzz.trimf(bike_count.universe, [7, 15, 23])
bike_count['high'] = fuzz.trapmf(bike_count.universe, [15, 23, 30, 30])

# for cars
# DATA : Observation
car_count['low'] = fuzz.trapmf(car_count.universe, [0, 0, 3, 9])
car_count['medium'] = fuzz.trimf(car_count.universe, [3, 9, 15])
car_count['high'] = fuzz.trapmf(car_count.universe, [9, 15, 21 ,21])

# for road width
# DATA : openrequest.form.tasikmalayakota.go.id
road_width['narrow'] = fuzz.trapmf(road_width.universe, [2, 2, 3, 5])
road_width['medium'] = fuzz.trapmf(road_width.universe, [3, 5, 7, 9])
road_width['wide'] = fuzz.trapmf(road_width.universe, [7, 9, 10, 10])


# for green light
# include delay

# DATA : Observation
green_light['short'] = fuzz.trapmf(green_light.universe, [5,5, 10, 25])
green_light['medium'] = fuzz.trimf(green_light.universe, [10, 25, 30])
green_light['long'] = fuzz.trapmf(green_light.universe, [25, 30, 35, 35])

bike_count.view()
car_count.view()
green_light.view()
road_width.view()

# car cound high

rule1 = ctrl.Rule(bike_count['high'] & car_count['high'] & road_width['wide'], green_light['medium'])
rule2 = ctrl.Rule(bike_count['high'] & car_count['high'] & road_width['medium'], green_light['long'])
rule3 = ctrl.Rule(bike_count['high'] & car_count['high'] & road_width['narrow'], green_light['long'])

rule4 = ctrl.Rule(bike_count['medium'] & car_count['high'] & road_width['wide'], green_light['medium'])
rule5 = ctrl.Rule(bike_count['medium'] & car_count['high'] & road_width['medium'], green_light['long'])
rule6 = ctrl.Rule(bike_count['medium'] & car_count['high'] & road_width['narrow'], green_light['long'])

rule7 = ctrl.Rule(bike_count['low'] & car_count['high'] & road_width['wide'], green_light['short'])
rule8 = ctrl.Rule(bike_count['low'] & car_count['high']& road_width['medium'], green_light['medium'])
rule9 = ctrl.Rule(bike_count['low'] & car_count['high']& road_width['narrow'], green_light['long'])

# car count med
rule10 = ctrl.Rule(bike_count['high'] & car_count['medium'] & road_width['wide'], green_light['short'])
rule11 = ctrl.Rule(bike_count['high'] & car_count['medium'] & road_width['medium'], green_light['long'])
rule12 = ctrl.Rule(bike_count['high'] & car_count['medium'] & road_width['narrow'], green_light['long'])

rule13 = ctrl.Rule(bike_count['medium'] & car_count['medium'] & road_width['wide'], green_light['short'])
rule14 = ctrl.Rule(bike_count['medium'] & car_count['medium'] & road_width['medium'], green_light['medium'])
rule15 = ctrl.Rule(bike_count['medium'] & car_count['medium'] & road_width['narrow'], green_light['long'])

rule16 = ctrl.Rule(bike_count['low'] & car_count['medium'] & road_width['wide'], green_light['short'])
rule17 = ctrl.Rule(bike_count['low'] & car_count['medium'] & road_width['medium'], green_light['medium'])
rule18 = ctrl.Rule(bike_count['low'] & car_count['medium'] & road_width['narrow'], green_light['long'])

# car count low
rule19 = ctrl.Rule(bike_count['high'] & car_count['low'] & road_width['wide'], green_light['short'])
rule20 = ctrl.Rule(bike_count['high'] & car_count['low'] & road_width['medium'], green_light['medium'])
rule21 = ctrl.Rule(bike_count['high'] & car_count['low'] & road_width['narrow'], green_light['long'])

rule22 = ctrl.Rule(bike_count['medium'] & car_count['low'] & road_width['wide'], green_light['short'])
rule23 = ctrl.Rule(bike_count['medium'] & car_count['low'] & road_width['medium'], green_light['medium'])
rule24 = ctrl.Rule(bike_count['medium'] & car_count['low'] & road_width['narrow'], green_light['long'])

rule25 = ctrl.Rule(bike_count['low'] & car_count['low'] & road_width['wide'], green_light['short'])
rule26 = ctrl.Rule(bike_count['low'] & car_count['low'] & road_width['medium'], green_light['short'])
rule27 = ctrl.Rule(bike_count['low'] & car_count['low'] & road_width['narrow'], green_light['medium'])

# Control System Creation and Simulation
traffic_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
traffic_simulation = ctrl.ControlSystemSimulation(traffic_ctrl)

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        bike_in = min(max(int(request.form.get("bike_count", 0)), 0 ), 0)
        car_in = min(max(int(request.form.get("car_count", 0)), 0), 100)
        road_in = min(max(int(request.form.get("road_width",2)),2), 10)

        traffic_simulation = ctrl.ControlSystemSimulation(traffic_ctrl)

        traffic_simulation.input['bike_count'] = bike_in
        traffic_simulation.input['car_count'] = car_in
        traffic_simulation.input['road_width'] = road_in

        # Compute the result
        traffic_simulation.compute()
        green_light_duration = traffic_simulation.output['green_light']
    
        # Return the result as JSON
        return render_template('index.html', grnlght=green_light_duration)
    return render_template('index.html', grnlght=0)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
