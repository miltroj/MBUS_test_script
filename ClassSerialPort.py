import serial
import datetime
from functools import reduce
# from statis_functions import StaticMethods
from additional_methods import *
from plot import *

dict_frames = { 0x56 : "Dane aktualne ", 0x60 : "Szczegoly zdarzen ",0x70 : "Szczegoly zdarzen ", 0x52: "Konfiguracja i progi ", 0x40 : "Dane serwisowe ", 0x5B : "Zapytanie 0x7B",
                0x7B : "Zapytanie 0x5B", 0x09 : "Update czasu ", 0x06: "wpis do rejestru", 0x0b : "Ustawienie adresu wild card", 0x20 : "Nieznana",
                0x05 : "przejscie do trybu normalnej pracy", 0x04 : "Ustaw dane do odczytu", 0x03: 'Zmiana bauduratu', 0x50 : "Szczegoly zdarzen", 0x30 : "Szczegoly zdarzen"}

def check_key(dict,key):
    if key in dict:
        return dict[key]
    else:
        return hex( key )

def date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f") + " "

def additional_log(respond):
    with open("log/respondLog-{}.txt".format(date_time_log_file()), 'a') as file:
        temp_string = "{}".format( hex(respond) )
        file.write(date_time() + "| respond |" + temp_string + " |" + "\n")

def additional_log_2(respond , info):
    with open("log/respondLog-{}.txt".format(date_time_log_file()), 'a') as file:
        temp_string = "{}".format( respond )
        file.write(date_time() + "| respond |" + info + temp_string + " |" + "\n")

def date_time_log_file():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def log_to_file_write(func):
    def func_wrapper(self, frame):
        temp_table = [ord(byte) for byte in frame]
        temp_frame_string = " ".join(format(byteInt, '02x') for byteInt in temp_table).upper()
        with open("log/loger-{}.txt".format(date_time_log_file()), 'a') as file:
            file.write(date_time() + " SND " + check_key(dict_frames,key=temp_table[1]) + " |" + parse_time_04_6D(temp_table) + "\n")
        with open("log/log_raw-{}.txt".format(date_time_log_file()) , 'a') as file_raw:
            file_raw.write( date_time() + temp_frame_string + "\n")
        return func(self , frame)
    return func_wrapper

def log_to_file_read(func):
    def func_wrapper(self):
        temp_table = func(self)
        temp_dict = False
        if type(temp_table) is ( list or int):
            if type(temp_table) == list and len(temp_table) > 1:
                temp_frame_string = " ".join(format(byteInt, '02x') for byteInt in temp_table).upper()
                temp_dict = True
            elif temp_table[0] <= 0xFF:
                # print "index %r %r" %(temp_table , type(temp_table[0]))
                temp_frame_string = format(temp_table[0], '02x').upper()
            else:
                # print "index %r %r" %(temp_table , type(temp_table))
                temp_frame_string = " przekroczono liczbe bajtow wejsciowych {}".format( temp_table )
            with open("log/loger-{}.txt".format(date_time_log_file()), 'a') as file:
                temp_insert = check_key(dict_frames,key=temp_table[1]) if temp_dict else "ACK"
                file.write( date_time() + " RCV  " + temp_insert + " |" + parse_time_04_6D(temp_table)  + "\n" )
            with open("log/log_raw-{}.txt".format(date_time_log_file()), 'a') as file_raw:
                file_raw.write(date_time() + temp_frame_string + "\n")
        else:
            print "     None nie wpisujemy do logowania %r" % type(temp_table)
        return temp_table
    return func_wrapper

class PortC(object):

    def __init__(self, port, baud):
        self.baudrate   = int(baud)
        self.port       = port
        self.com        = serial.Serial(self.port , baudrate=self.baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,timeout=.2)
        print "Otwarto port"
        self.table      = []

        #region chart
        self.dt_flow         = []
        self.x_val_AVG_flow  = []
        self.x_val_all_flow  = []
        self.x_events_saved  = []
        self.x_events_actual = []
        self.y_date_time     = []
        self.slep_time_building = 1
        #endregion

    def reinit_COM_port(self, baudurate):
        print("Reinicjalizacja portu bd=%r" %baudurate)
        self.com.close()
        self.com        = serial.Serial(self.port , baudrate=baudurate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,timeout=.1)

    def write_to_file(self, datetime, avg, all):
        with open("charts/charts-{}.txt".format(date_time_log_file()) , 'a') as file_raw:
            events_saved = ';'.join( str(i) for i in self.x_events_saved[-1])
            events_actual = ';'.join( str(i) for i in self.x_events_actual[-1])
            # file_raw.write( datetime.strftime("%Y-%m-%d %H:%M:%S:%f") + ";" + str(avg) + ";" + str(all) + "\n")
            file_raw.write( datetime.strftime("%Y-%m-%d %H:%M:%S:%f") + ";" + str(avg) + ";" + str(all) + ";" + events_saved + ";" + events_actual + "\n")

    @log_to_file_write
    def write(self, frame):
        self.com.flushInput()
        self.com.write(frame)
        # print "Wyslano " + frame[0:2]
        if list(frame):
            print date_time() + "Wyslano %r"  %" ".join(hex(ord(element)) for element in frame)
        else:
            print date_time() + "Wyslano %r"  %hex(ord(frame[0]))

    @log_to_file_read
    def readACK(self):
        while True:
            if self.com.inWaiting() == 0:
                return None
            response = self.com.read()
            print date_time() + "ACK %r" %hex(ord(response))
            return ord(response)

    @log_to_file_read
    def read_2(self):
        self.table = []
        while True:
            if self.com.inWaiting() == 0:
                return None
            # print "Oczekuje w buforze %d" %self.com.inWaiting()
            response = self.com.read(1)
            # print "{} len {}".format( hex(ord(response)) , len(self.table) )
            # print "{} len {}".format( ord(response) , len(self.table) )
            # if type(ord(response)) == int:
            self.table.append(ord(response))
            # print int(self.table[0],16)
            if len(self.table) > 2:
                if self.table[1] + 6 == len(self.table) and self.table[0] == 0x68:
                    print(date_time() + "Odczytano %r" %" ".join(format(byteInt, '02x') for byteInt in self.table).upper() )
                    print(date_time() + "Suma kontrolna %r" %hex(self.table[-2]))
                    print(date_time() + "CrC check      %r" %self.crcCheck())
                    return self.table

    @log_to_file_read
    def read_3(self):
        self.table = []
        x = 0
        while True:
            if self.com.inWaiting() == 0 and x > 15:
                # additional_log_2(" " ,"Wejscie w brak odpowiedzi")
                break
            elif self.com.inWaiting() != 0:
                response = ord(self.com.read(1))
                # additional_log( response )
                self.table.append(response)
                # additional_log_2(" " ,"Wejscie w append")

                if response == 0xE5:
                    # additional_log_2(" ", "Wejscie w ACK")
                    return self.table
                elif len(self.table) > 2:
                    if self.table[1] + 6 == len(self.table) and self.table[0] == 0x68:
                        print(date_time() + "Odczytano %r" %" ".join(format(byteInt, '02x') for byteInt in self.table).upper() )
                        print(date_time() + "Suma kontrolna %r" %hex(self.table[-2]))
                        print(date_time() + "CrC check      %r" %self.crcCheck())
                        # additional_log_2(" ", "Wejscie w odczyt")
                        return self.table

            x += 1
            # additional_log_2(" " ," INKREMENTACJA x {}".format(x))


    def read_all(self):
            self.table = []
            self.recived = []
            x = 0
            while True:
                time.sleep(.2)
                if self.com.inWaiting() != 0:
                    self.recived = [ord(element) for element in self.com.read()]
                    # additional_log_2(" ", "Odpowiedzi %r" %" ".join(format(byteInt, '02x') for byteInt in self.recived ).upper())
                    return self.table
                else:
                    break
                # x += 1
                # additional_log_2(" ", " INKREMENTACJA x {}".format(x))

            # if response == 0xE5:
            #     return self.table

            # elif len(self.table) > 2:
            #     if self.table[1] + 6 == len(self.table) and self.table[0] == 0x68:
            #         print(date_time() + "Odczytano %r" %" ".join(format(byteInt, '02x') for byteInt in self.table).upper() )
            #         print(date_time() + "Suma kontrolna %r" %hex(self.table[-2]))
            #         print(date_time() + "CrC check      %r" %self.crcCheck())
            #         return self.table
            """
                else:
                    print(date_time() + "Ramka niezidentyfikowana %r" % " ".join(format(byteInt, '02x') for byteInt in self.table).upper())
                    print(date_time() + "Suma kontrolna %r" %hex(self.table[-2]))
                    print(date_time() + "CrC check      %r" %self.crcCheck())
                    return self.table
            """

    def write_and_read(self, frame):
        self.write(frame)
        tab_events = []
        time.sleep(0.2)
        temp_read = self.read_3()
        all_variable, avg_variable, tab_events, dt_flow = iterate_and_find( temp_read )
        # if temp_read != None:
        #     print "Parsed time %r \n" %parse_time_04_6D( temp_read )
        # if all_variable is not None and avg_variable is not None is:
        if (all_variable and avg_variable and tab_events) is not None:
            self.dt_flow.append( dt_flow )
            self.x_val_AVG_flow.append( avg_variable )
            self.x_val_all_flow.append( all_variable )
            self.x_events_saved.append( tab_events[:16])
            # print("     SAVED EVENTS %r" %tab_events[:16])
            self.x_events_actual.append( tab_events[16:])
            # print("     actual EVENTS %r" %tab_events[16:])
            self.y_date_time.append( datetime.datetime.now() )
            self.write_to_file( datetime.datetime.now() ,avg_variable , all_variable)

    def write_and_read_baudurate(self, frame, baudurate):
        self.write(frame)
        time.sleep(0.5)
        pom = self.read_3()
        if pom != None: print "Baudurate changed %r\n" %baudurate

    def returnTable(self):
        print "Returned table %r" %" ".join(format(byteInt, '02x') for byteInt in self.table).upper()
        self.table = []

    def crcCheck(self):
        tempTable = self.table[4:len(self.table)-2]
        return hex(reduce(lambda a, b: (a + b) & 0xFF, tempTable, 0))

    def close(self):
        self.com.close()
        print "Zamknieto port"

    def build_chart(self):
        print ("Dt sleep %r" %self.dt_flow)
        print ("Dt sleep %r" %type(self.dt_flow))
        print ("time %r" %self.y_date_time)
        sleep_time = self.slep_time_building
        create_dt_flow(self.dt_flow, self.y_date_time)
        time.sleep(sleep_time)
        create_avg_flow_chart(self.x_val_AVG_flow, self.y_date_time)
        create_overall_flow_chart(self.x_val_all_flow, self.y_date_time)
        create_chart_events(self.x_events_saved, self.y_date_time)
        time.sleep(sleep_time)
        create_chart_events(self.x_events_actual, self.y_date_time)

    def build_chart_act_events(self):
        create_chart_events(self.x_events_actual, self.y_date_time)
        time.sleep(self.slep_time_building)

    def build_chart_svd_events(self):
        create_chart_events(self.x_events_saved, self.y_date_time)
        time.sleep(self.slep_time_building)

    def build_ch_avg_flow(self):
        create_avg_flow_chart(self.x_val_AVG_flow, self.y_date_time)
        time.sleep(self.slep_time_building)

    def build_ch_all_flow(self):
        create_overall_flow_chart(self.x_val_all_flow, self.y_date_time)
        time.sleep(self.slep_time_building)

    def build_ch_dt(self):
        create_dt_flow(self.x_val_all_flow, self.y_date_time)
        time.sleep(self.slep_time_building)



    if __name__ == "__main__":
        pass