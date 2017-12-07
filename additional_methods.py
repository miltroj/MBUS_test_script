import plotly.offline as offline

def parse_time(byte_table):
    bajt1, bajt2, bajt3,bajt4 = byte_table
    wal             = {0: "walid", 1: "invalid"}
    walidation      = (bajt1 & 0x80) >> 6
    minutes         = bajt1 & 0x3F
    counting_period = (bajt2 & 0x80) >> 7
    wiek            = (bajt2 & 0x60) >> 5
    hours           = bajt2 & 0x1F
    year            = ((bajt4 & 0xF0) >> 1) + ((bajt3 & 0xE0) >> 5)
    day             = bajt3 & 0x1F
    month           = bajt4 & 0x0F
    # print(bajt4)
    count_year       = 1900 + 100 * int(wiek) + int(year)
    parsed_value_str= "{:02}/{:02}/{:02} {:02}:{:02}  counting period:{} wiek:{} walidation:{}".format( day, month, year, hours,minutes, counting_period, count_year,wal[walidation] )
    return parsed_value_str

def parse_time_04_6D(frame):
    date_time_found = False
    temp_table = []
    if type(frame) == int:
        return ''

    for i,element in enumerate(frame):
        if element == 0x04 and frame[i+1] == 0x6D:
            temp_table = [frame[ (i+2) +byte] for byte in range(4)]
            # print "tab %r i=%r" %(temp_table,i)
            date_time_found = True
            break
        # elif element == 0x04 and frame[i+1] == 0x16:

    if date_time_found:

        bajt1, bajt2, bajt3,bajt4 = temp_table
        wal             = {0: "walid", 1: "invalid"}
        walidation      = (bajt1 & 0x80) >> 6
        minutes         = bajt1 & 0x3F
        counting_period = (bajt2 & 0x80) >> 7
        wiek            = (bajt2 & 0x60) >> 5
        hours           = bajt2 & 0x1F
        year            = ((bajt4 & 0xF0) >> 1) + ((bajt3 & 0xE0) >> 5)
        day             = bajt3 & 0x1F
        month           = bajt4 & 0x0F
        # print(bajt4)
        count_year       = 1900 + 100 * int(wiek) + int(year)
        parsed_value_str= "{:02}/{:02}/{:02} {:02}:{:02}  counting period:{} wiek:{} walidation:{}".format( day, month, year, hours,minutes, counting_period, count_year,wal[walidation] )
        return parsed_value_str
    return " time---"

def create_frame(frame):
    returned_temp = ''
    for element in frame:
        returned_temp += chr(element)
    # print("%r" %returned_temp)
    return returned_temp

def flow_all(element,i,frame):
    # print("{} {} {}".format(element,i,frame[i+1]))
    if len(frame) - len( frame[:i] )  > 5:
        if element == 0x04 and frame[i + 1] == 0x16:
            temp_overall = [frame[i + 2 + byte] for byte in range(4)]
            # print("all %r" %temp_overall)
            # print("avg %r" %temp_avg)
            all_b1, all_b2, all_b3, all_b4 = temp_overall
            int_all = all_b1 + (all_b2 << 8) + (all_b3 << 16) + (all_b4 << 24)
            # print("all %r" %int_avg)
            # print("avg %r" %int_all)
            return int_all, False
        else:
            return None, True
    else:
        return None, True

def flow_avg(element,i,frame):
    # print("{} {} {}".format(element,i,frame[i+1]))
    if len(frame) - len( frame[:i] )  > 5:
        if element == 0x02 and frame[i + 1] == 0x3E:
            temp_avg = [frame[i + 2 + byte] for byte in range(2)]
            # print("all %r" %temp_overall)
            # print("avg %r" %temp_avg)
            avg_b1, avg_b2 = temp_avg
            int_avg = avg_b1 + (avg_b2 << 8)
            # print("all %r" %int_avg)
            # print("avg %r" %int_all)
            return int_avg, False
        else:
            return None, True
    else:
        return None, True

def iterate_and_find(frame):
    int_all_exist = True
    int_avg_exist = True
    if type(frame) == int or frame == None:
        return None, None
    for i,element in enumerate(frame):
        if int_all_exist:
            int_all, int_all_exist = flow_all(element,i,frame)
        if int_avg_exist:
            int_avg, int_avg_exist = flow_avg(element,i,frame)
        else:
            break
    return int_all, int_avg

def create_chart(y1, y2, x_time):
    offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw chwilowy'},
                           {'y': y2, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw calkowity'}],
                  'layout': {'title': 'Przeplywy',
                             'font': dict(size=16)}})

if __name__ == '__main__':

    string = '68 56 56 68 08 04 72 00 00 00 00 01 06 15 07 26 88 00 00 0C 78 00 00 00 00 04 6D 36 A9 21 2C 04 16 FB 00 00 00 02 3E 5A 00 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 67 16'
    string2 = '68 56 56 68 08 04 72 00 00 00 00 01 06 15 07 26 88 00 00 0C 78 00 00 00 00 04 6D 36 A9 21 2C 04 16 FF FF FF FF 02 3E FF FF 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 67 16'
    string3 = '2C 04 11 FF FF FF FF 02 31 FF FF 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 04 16'
    table = string2.split(" ")
    table_int = [int(element,16) for element in table]
    # tablica = [0x02, 0x0A, 0x11, 0x22]
    #
    # print(StaticMethods.parse_time(tablica))
    #
    print("%r" %table)
    print("%r" %table_int)
    print (iterate_and_find(table_int) )
