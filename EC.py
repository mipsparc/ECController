#coding: utf8

class EC:
    CARS = {
        'e655': {'desc': 'DCCの交直流特急型電車', 'type': 'dcc'},
        'e233_dc': {'desc': 'アナログの直流通勤型電車', 'type': 'dc'},
        'de10': {'desc': 'DCCの液体式ディーゼル機関車', 'type': 'dcc'},
    }
    
    def __init__(self, ectype):
        # 入力値の検証
        if ectype in self.CARS:
            self.ectype = ectype
            self.dcc = self.CARS[ectype]['type'] == 'dcc'
        else:
            raise ValueError
        
        self.speed_level = 0
    
    def isDcc(self):
        return self.dcc
    
    def getCars(self):
        return self.CARS
    
    def calcSpeed(self, accel_knotch, brake_knotch):
        if self.ectype == "e655":
            return self.e655(accel_knotch, brake_knotch)
        elif self.ectype == 'e233_dc':
            return self.e233_dc(accel_knotch, brake_knotch)
        else:
            raise ValueError
    
    def e655(self, accel_knotch, brake_knotch): 
        BASE_LEVEL = 80

        accel_level = accel_knotch * 0.4
        if self.speed_level < 300:
            accel_level = accel_knotch * 0.2
        else:
            accel_level = accel_knotch * 0.05
        
        brake_level = brake_knotch * 0.6
        self.speed_level = self.speed_level + accel_level - brake_level
        
        if self.speed_level > 0:
            return self.speed_level + BASE_LEVEL
        elif self.speed_level > 800:
            return 800
        
        self.speed_level = 0
        return 0
    
    def e233_dc(self, accel_knotch, brake_knotch):
        BASE_LEVEL = 180

        if self.speed_level < 70:
            accel_level = accel_knotch * 0.5
        elif self.speed_level < 220:
            accel_level = accel_knotch * 0.3
        elif self.speed_level < 320:
            accel_level = accel_knotch * 0.2
        else:
            accel_level = accel_knotch * 0.05
        
        brake_level = brake_knotch * 0.4
        self.speed_level = self.speed_level + accel_level - brake_level
        
        if self.speed_level > 0:
            return self.speed_level + BASE_LEVEL
        elif self.speed_level > 800:
            return 800
        
        self.speed_level = 0
        return 0
