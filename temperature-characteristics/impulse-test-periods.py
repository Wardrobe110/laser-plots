def fun():
    #All in milimeters and seconds
    object_len = 100
    sintering_las_d = 0.2
    heating_las_d = 8
    #20% && 30%
    manufacturing_v = 1000
    homing_v =2
    
    processing_t = object_len / manufacturing_v
    times_sintering = object_len / sintering_las_d
    single_sintering_t = processing_t / times_sintering
    times_heating_before_sintering = (heating_las_d / 2) / 0.2
    heating_before_sintering_t = times_heating_before_sintering * single_sintering_t
    
    downtime_t = processing_t - heating_before_sintering_t
    
    print(f"======= For manufacturing speed {manufacturing_v} [mm/s] =======")
    print(f"One horizontal line processing time: {processing_t} [s]")
    print(f"Times we will sinter during that time: {times_sintering} [-]")
    print(f"Single sintering will take: {single_sintering_t} [s]")
    print(f"Point will be heated {times_heating_before_sintering} times before sintering")
    print(f"Heating time before sintering {heating_before_sintering_t} [s]")
    print(f"Heating downtime per line {downtime_t} [s]")
    


if __name__ == "__main__":
    fun()
