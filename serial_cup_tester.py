import serial
import time
import struct
import datetime
from serial.serialutil import SerialException
from additional_methods import *
from threading import Thread

def date_time_log_file():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f") + " "

def log_to_file_write_speed(func):
    def func_wrapper(self, table):
        temp_string = " speed:{}    time_delay:{}".format(table[0],table[1])
        temp_fun = func(self, table)
        with open("speeds/speeds-{}.txt".format(date_time_log_file()), 'a') as file:
            file.write(date_time() + temp_string + " send:" + str(temp_fun) + "\n")
        return temp_fun
    return func_wrapper

def create_char(table):
    temp_to_ret =''
    for element in table:
        temp_to_ret += chr( element )
    return temp_to_ret

class Cup_tester(object):

    def __init__(self,port,test_scenario):
        self.port = port
        self.test = test_scenario
        self.com  = serial.Serial(self.port , baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE,timeout=.2,)
        self.id_number = 0
        print "Otwarto port komunikacyjny - tester nakladek {}".format(self.port)
        self.communication_table = [self.id_number,0x00,0x00,0x00, 0x50,0x00,0x00,0x00, 0x00,0x00,0x40, 0x40]
        # self.print_after = datetime.datetime.now() + datetime.timedelta(hours=self.print_every)
        self.date_now = datetime.datetime.now()

        self.start_speed = 0
        self.unloop_cup_test = False
        self.sent_counter = 0
        self.actual_speed = None

    # def write(self,tab=[1,2,3], start =0, step = 3):
    def create_frame(self):
        return create_char(self.communication_table)

    def time_delta(self,d_time):
        return self.date_now + datetime.timedelta(seconds=d_time)

    def change_speed(self, speed_to_change):
        temp_speed_arry = bytearray(struct.pack('f', speed_to_change))
        for i in range(8,12):
            self.communication_table[i] = temp_speed_arry[i-8]
        # print ("%d %r" %(datetime.datetime.now(),self.communication_table))
        print ("{} {}".format(datetime.datetime.now(),self.communication_table))

    def increment_ID_and_time(self):
        self.id_number += 1
        self.date_now = datetime.datetime.now()
        byte_arraya = bytearray( struct.pack('<i', self.id_number) )
        for i in range(4):
            self.communication_table[i] = byte_arraya[i]

    def write_speed_time(self, val_to_change):
        self.change_speed(val_to_change[0])
        temp_to_send = self.create_frame()
        self.com.write( temp_to_send )
        self.increment_ID_and_time()
        # time.sleep(val_to_change[1])

    def write_speed_time_while(self, val_to_change):
        # print ("%r %r " %(self.date_now, self.time_delta(val_to_change[1])))
        if datetime.datetime.now() > self.time_delta(val_to_change[1]):
            self.change_speed(val_to_change[0])
            temp_to_send = self.create_frame()
            self.com.write( temp_to_send )
            self.increment_ID_and_time()
            return True
        return False

    # def write_steps_from_table(self):
    #     i = 0
    #     while True:
    #         if i == 0:
    #             self.write_speed_time(self.test[i])
    #             i+=1
    #
    #         elif self.write_speed_time_while(self.test[i]):
    #             i+= 1
    #             if i == len(self.test):
    #                 print (self.test[-1][1])
    #                 time.sleep( self.test[-1][1] )
    #                 i= 0
    #                 # break

    @log_to_file_write_speed
    def write_speed_delay(self, val_to_change):
        if len(val_to_change) is 0:
            time.sleep(10)
            return False
        self.change_speed(val_to_change[0])
        temp_to_send = self.create_frame()
        try:
            self.com.write( temp_to_send )
            self.increment_ID_and_time()
        except SerialException:
            print ("Cos poszlo nie tak w wysylaniu")
            time.sleep(2)
            return False
        time.sleep(val_to_change[1])
        return True

    def write_reset(self):
        # self.communication_table = [self.id_number,0x00,0x00,0x00, 0x50,0x00,0x00,0x00, 0x00,0x00,0x40, 0x40]
        cleared_table = [ 0 for i in range( len(self.communication_table) )]
        print ('%r' %cleared_table)
        temp_to_send = create_char( cleared_table )
        self.com.write( temp_to_send )
        self.increment_ID_and_time()
        print ("Cos poszlo nie tak w wysylaniu")
        time.sleep(2)
        return True

    # def while_write(self):
    #     i=0
    #     while True:
    #         print("%r" %self.test[i])
    #         if is_list_empty(self.test,self.test) is False:
    #             # print("List is empty {}".format(i))
    #             continue
    #         try:
    #             if self.write_speed_delay( self.test[i] ):
    #                 i+= 1
    #                 if i == len(self.test) and self.loop_cup_test:
    #                     break
    #                 if i == len(self.test):
    #                     i=0
    #         except:
    #             print('Continue {} tests {}'.format(i,self.test))
    #             time.sleep(10)
    #             continue

    def count_test_scenarios(self):
        return len(self.test) - 1

    def start_from_zero(self):
        self.sent_counter = 0
        print "{} Wysylam predkosc od poczatku".format(date_time())

    def increment_send_counter(self):
        self.actual_speed = self.test[self.sent_counter]
        if self.sent_counter == self.count_test_scenarios():
            self.start_from_zero()
        else:
            self.sent_counter += 1

    def while_write(self):
        while True:
            i = self.sent_counter
            temp_test_cases = self.test
            if is_list_empty(temp_test_cases,temp_test_cases) is False:
                # print("List is empty {}".format(i))
                continue
            try:
                if self.write_speed_delay( temp_test_cases[i] ):
                    self.increment_send_counter()
                    if i == self.count_test_scenarios() and self.unloop_cup_test:
                        break
            except:
                print('Continue {} tests {}'.format(i,self.test))
                time.sleep(10)
                continue


    def stop_speed(self):
        self.communication_table[-2] = 0
        self.communication_table[-1] = 0
        temp_to_send = self.create_frame()
        self.com.write( temp_to_send )
        self.increment_ID_and_time()
        time.sleep(3)

    def close(self):
        self.com.close()



if __name__ == "__main__":

    port = "COM11"

    scenarois_from_file = table_of_speeds_from_file("scenarios/testowy.txt")

    speeds = []
    cuptest = Cup_tester(port,scenarois_from_file)

    cuptest.unloop_cup_test = True
    cuptest.while_write()

    cuptest.stop_speed()
    cuptest.close()
