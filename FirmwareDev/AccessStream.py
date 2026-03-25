from pymavlink import mavutil

class AccessStream():
    def __init__(self, port = '/dev/serial0', baud = 115200):
        try:
            self.port = port
            self.baud = baud
            self.master = mavutil.mavlink_connection(port, baud=baud)
            self.master.wait_heartbeat()
        except:
            return "Error init"
    
    def log_telemtry(mmsg, msg_type):
        
                if msg_type == "GPS_RAW_INT":
                    print(f"[GPS] Lat:{msg.lat/1e7:.6f} Lon:{msg.lon/1e7:.6f} "
                        f"Alt:{msg.alt/1000:.2f}m Sats:{msg.satellites_visible}")

                elif msg_type == "ATTITUDE":
                    print(f"[ATTITUDE] Roll:{msg.roll:.2f} Pitch:{msg.pitch:.2f} Yaw:{msg.yaw:.2f}")

        
                elif msg_type == "SCALED_IMU2" or msg_type == "SCALED_IMU":
                    print(f"[MAG] X:{msg.xmag} Y:{msg.ymag} Z:{msg.zmag}")

        
                elif msg_type == "RC_CHANNELS":
                    print(f"[RC] CH1:{msg.chan1_raw} CH2:{msg.chan2_raw} "
                        f"CH3:{msg.chan3_raw} CH4:{msg.chan4_raw}")

        
                elif msg_type == "SERVO_OUTPUT_RAW":
                    print(f"[OUTPUT] S1:{msg.servo1_raw} S2:{msg.servo2_raw} "
                        f"S3:{msg.servo3_raw} S4:{msg.servo4_raw}")

        
                elif msg_type == "SYS_STATUS":
                    voltage = msg.voltage_battery / 1000.0
                    print(f"[POWER] {voltage:.2f}V")
                
                elif msg_type == "VFR_HUD":
                    print(f"[NAV] Alt:{msg.alt:.2f}m "
                        f"GroundSpeed:{msg.groundspeed:.2f}m/s "
                        f"Climb:{msg.climb:.2f}m/s")

                elif msg_type == "HEARTBEAT":
                    print("[HEARTBEAT]")

    def get_data_stream(self, content, continous):
        
        if continous:
            while True:
                msg = self.master.recv_match(blocking=True)
                if not msg:
                    continue

                msg_type = msg.get_type()

        else:
            