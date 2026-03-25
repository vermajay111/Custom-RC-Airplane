from pymavlink import mavutil

class ControlHardware:
    def __init__(self, port='/dev/serial0', baud=115200):
        try:
            self.master = mavutil.mavlink_connection(port, baud=baud)
            self.master.wait_heartbeat()
        except Exception as e:
            raise RuntimeError(f"Failed to init connection: {e}")
    
    def get_driver_inputs(self):
       
        msg = self.master.recv_match(type='RC_CHANNELS', blocking=True)
            
        if not msg:
            return

        return {
                "ch1": msg.chan1_raw, 
                "ch2": msg.chan2_raw, 
                "ch3": msg.chan3_raw, 
                "ch4": msg.chan4_raw  
        }
    
    def override_rc(self, ch1=65535, ch2=65535, ch3=65535, ch4=65535):
        """
        This function allows us to change the power of the thurster motor
        """

        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            ch1, ch2, ch3, ch4, # ch3 manages speed
            65535, 65535, 65535, 65535 # these are the AUX switches on the remote
        )

        #each one of the values ch1, 2... etc are linked to a certain think like so: sterring, pitch, throttle, yaw setting them to the max 16 bit max unsigned integer tells the F.C to ignore the python script and follow the command given by the remote
    
    def set_servo(self, servo_number, pwm_value):

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,       
            servo_number, 
            pwm_value,    
            0, 0, 0, 0, 0 
        )
        return True

    def get_data_stream(self):
        while True:
            msg = self.master.recv_match(blocking=True)
            if not msg:
                continue

            msg_type = msg.get_type()

            if msg_type == "GPS_RAW_INT":
                return {
                    "lat": msg.lat / 1e7,
                    "lon": msg.lon / 1e7,
                    "alt": msg.alt / 1000.0,
                    "sats": msg.satellites_visible
                }

            elif msg_type == "ATTITUDE":
                return {
                    "roll": msg.roll,
                    "pitch": msg.pitch,
                    "yaw": msg.yaw
                }

            elif msg_type in ("SCALED_IMU", "SCALED_IMU2"):
                return {
                    "xmag": msg.xmag,
                    "ymag": msg.ymag,
                    "zmag": msg.zmag
                }

            elif msg_type == "RC_CHANNELS":
                return {
                    "ch1": msg.chan1_raw,
                    "ch2": msg.chan2_raw,
                    "ch3": msg.chan3_raw,
                    "ch4": msg.chan4_raw
                }

            elif msg_type == "SERVO_OUTPUT_RAW":
                return {
                    "s1": msg.servo1_raw,
                    "s2": msg.servo2_raw,
                    "s3": msg.servo3_raw,
                    "s4": msg.servo4_raw
                }

            elif msg_type == "SYS_STATUS":
                return {
                    "voltage": msg.voltage_battery / 1000.0
                }

            elif msg_type == "VFR_HUD":
                return {
                    "alt": msg.alt,
                    "groundspeed": msg.groundspeed,
                    "climb": msg.climb
                }

            elif msg_type == "HEARTBEAT":
                return {"heartbeat": True}
            