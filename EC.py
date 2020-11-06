#coding: utf8

class EC:
    def __init__(self, ectype):
        if ectype == "e531":
            self.ectype = "e531"
        if ectype == "e655":
            self.ectype = "e655"
        else:
            raise ValueError
    
    def calcSpeed(self, current_speed_level, accel_knotch, brake_knotch):
        if self.ectype == "e531":
            return self.e531(current_speed_level, accel_knotch, brake_knotch)
        if self.ectype == "e655":
            return self.e655(current_speed_level, accel_knotch, brake_knotch)
        else:
            raise ValueError
        
    def e531(self, current_speed_level, accel_knotch, brake_knotch):
        base_level = 67
        if 0 <= current_speed_level < base_level:
            speed_level = base_level
        
        if current_speed_level < 80:
            accel_level = accel_knotch * 0.4
        elif current_speed_level < 130:
            accel_level = accel_knotch * 0.3
        elif current_speed_level < 250:
            accel_level = accel_knotch * 0.2
        elif current_speed_level < 300:
            accel_level = accel_knotch * 0.1
        else:
            accel_level = accel_knotch * 0.05
        
        brake_level = brake_knotch * 0.4
        speed_level = current_speed_level + accel_level - brake_level
        
        if speed_level < base_level:
            speed_level = 0
        if speed_level > 400:
            speed_level = 400
        
        return speed_level
    
    
    def e655(self, current_speed_level, accel_knotch, brake_knotch):
        base_level = 80
        if 0 <= current_speed_level < base_level:
            current_speed_level = base_level
            
        speed_level = current_speed_level + accel_knotch * 0.4 - brake_knotch * 0.6

        if speed_level < base_level:
            speed_level = 0
        if speed_level > 400:
            speed_level = 400
       
        return speed_level

