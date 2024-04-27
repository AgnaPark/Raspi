from licence_plate import RoLicensePlate

if __name__ == "__main__":
    
    plate1 = RoLicensePlate("TM 99 ABC")
    print(f"Is 'TM 99 ABC' valid? {plate1.is_roLicensePlate()}\n")

    plate2 = RoLicensePlate("XY 12 ABC")
    print(f"Is 'XY 12 ABC' valid? {plate2.is_roLicensePlate()}\n")

    plate3 = RoLicensePlate("B 100 TOB")
    print(f"Is 'B 100 TOB' valid? {plate3.is_roLicensePlate()}\n")

    plate4 = RoLicensePlate("B 1234 ABC")
    print(f"Is 'B 1234 ABC' valid? {plate4.is_roLicensePlate()}\n")

    plate5 = RoLicensePlate("AB 123 ABC")
    print(f"Is 'AB 123 ABC' valid? {plate5.is_roLicensePlate()}\n")

    plate6 = RoLicensePlate("TM 24 ZOB")
    print(f"Is 'TM 24 ZOB' valid? {plate6.is_roLicensePlate()}\n")

    plate7 = RoLicensePlate("TM 24 ZOI")
    print(f"Is 'TM 24 ZOI' valid? {plate7.is_roLicensePlate()}\n")

    plate8 = RoLicensePlate("TM 24 ZOQ")
    print(f"Is 'TM 24 ZOQ' valid? {plate8.is_roLicensePlate()}\n")

    plate9 = RoLicensePlate("TM 24 III")
    print(f"Is 'TM 24 III' valid? {plate9.is_roLicensePlate()}\n")
    
    plate10 = RoLicensePlate("TM 24 OOO")
    print(f"Is 'TM 24 OOO' valid? {plate10.is_roLicensePlate()}\n")
    
    plate11 = RoLicensePlate("IF 098754")
    print(f"Is 'IF 098754' temporary short valid ? {plate11.is_roLicensePlate()}\n")
    
    plate17 = RoLicensePlate("IF 908754")
    print(f"Is 'IF 908754' temporary short valid ? {plate17.is_roLicensePlate()}\n")
    
    plate12 = RoLicensePlate("B 16095")
    print(f"Is 'B 16095' temporary long valid ? {plate12.is_roLicensePlate()}\n")
    
    plate18 = RoLicensePlate("B 06095")
    print(f"Is 'B 06095' temporary long valid ? {plate18.is_roLicensePlate()}\n")

    plate13 = RoLicensePlate("TC 157123")
    print(f"Is 'TC 157123' diplomatic valid ? {plate13.is_roLicensePlate()}\n")
    
    plate19 = RoLicensePlate("MR 127123")
    print(f"Is 'MR 127123' diplomatic valid ? {plate19.is_roLicensePlate()}\n")
    
    plate14 = RoLicensePlate("MAI 157123")
    print(f"Is 'MAI 157123' diplomatic  valid ? {plate14.is_roLicensePlate()}\n")
    