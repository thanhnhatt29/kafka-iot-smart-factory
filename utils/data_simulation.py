import random

def simulate_temperature():
    return round(random.uniform(20, 40), 2)

def simulate_humidity():
    return round(random.uniform(30, 90), 2)

def simulate_vibration():
    return round(random.uniform(0.1, 5.0), 2)