import time
from .ControlHardware import ControlHardware
        
HISTORY_LENGTH_SECONDS = 30
control_hardware = ControlHardware()

driver_control_history = []

def calculate_average(history):

    if len(history) == 0:
        return [1500, 1500, 1000, 1500]

    final = [0, 0, 0, 0]
    for item in history:
        final[0] += item['inputs']['ch1']
        final[1] += item['inputs']['ch2']
        final[2] += item['inputs']['ch3']
        final[3] += item['inputs']['ch4']
            
    for i in range(len(final)):
        final[i] /= len(history)
            
    return final

"""
Basic script that keeps a 30-second history of the driver's commands.
If the latest command is massively odd compared to the average, it detects an "erratic" move.
"""

print("Starting Erratic Driving Monitor...")

while True:
    current_time = time.time()
    driver_commands = control_hardware.get_driver_inputs()

    if driver_commands:

        record = {
            "timestamp": current_time,
            "inputs": driver_commands
        }
        driver_control_history.append(record)
        
        cutoff_time = current_time - HISTORY_LENGTH_SECONDS
        
        recent_history = []
        for record in driver_control_history:
            if record["timestamp"] > cutoff_time:
                recent_history.append(record)

        driver_control_history = recent_history
        avg_controls = calculate_average(driver_control_history)
        current_roll = driver_commands['ch1']
        average_roll = avg_controls[0]
        
        difference = abs(current_roll - average_roll)
        
        if difference > 300:
            print(f"ERRATIC MOVEMENT DETECTED! Dodging a tree?")
            print(f"Average Roll: {int(average_roll)} | Sudden Jump To: {current_roll}")
        else:
            print(f"Smooth flying. Average Roll: {int(average_roll)}")
             
    time.sleep(0.05)