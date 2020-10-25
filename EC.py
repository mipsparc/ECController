#coding: utf-8

class EC:
    def __init__(self, ectype):
        if ectype == "e531":
            self.ectype = "e531"
        else:
            raise ValueError
    
    def calcSpeed(self, current_speed_level, accel_knotch, brake_knotch):
        if self.ectype == "e531":
            return self.e531(current_speed_level, accel_knotch, brake_knotch)
        else:
            raise ValueError
        
    def e531(self, current_speed_level, accel_knotch, brake_knotch):
        if current_speed_level < 80:
            accel_level = accel_knotch * 0.25
        elif current_speed_level < 130:
            accel_level = accel_knotch * 0.2
        elif current_speed_level < 250:
            accel_level = accel_knotch * 0.15
        elif current_speed_level < 300:
            accel_level = accel_knotch * 0.1
        elif current_speed_level < 350:
            accel_level = accel_knotch * 0.05
        
        brake_level = brake_knotch * 0.4
        speed_level = current_speed_level + accel_level - brake_level
        if speed_level < 0:
            speed_level = 0
        if speed_level > 400:
            speed_level = 400
        
        return speed_level
