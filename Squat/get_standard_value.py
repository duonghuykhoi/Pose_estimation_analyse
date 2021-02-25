
#Return Standard_value and Standard_ratio_value of body-parts
def get_standard_value(data):
    
    sum = 0
    sum_ratio = 0
    count = 0
    min = 100000

    for i in data:              #i is body-parts coord [body-parts-coord, ankle-coord]
        #Get min coord of body-parts
        if i[0] < min:   
            min = i[0]
            count += 1
            sum += i[0]
            sum_ratio += i[0]/i[1]
    standard = (sum / count)
    standard = (standard + min) / 2
    standard_ratio = sum_ratio / count

    return abs(standard), abs(standard_ratio)