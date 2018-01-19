import datetime
import time
from additional_methods import *

class Commands(object):

    def __init__(self, mbus_port_COM, cup_port_COM ):
        self.commands = ""
        self.print_every = 4    #every h
        # self.print_after = self.datetime_now + datetime.timedelta(hours=self.print_every)
        self.print_after = datetime.datetime.now() + datetime.timedelta(hours=self.print_every)
        self.class_instance_Mbus = mbus_port_COM
        self.class_instance_Cup = cup_port_COM

    def build_all_charats(self):
        self.commands = ""
        self.class_instance_Mbus.build_chart()

    def build_flow_chart(self):
        self.commands=''
        self.class_instance_Mbus.build_ch_all_flow()

    def build_avg_speed_chart(self):
        self.commands = ''
        self.class_instance_Mbus.build_ch_avg_flow()

    def build_actual_events_chart(self):
        self.commands = ""
        self.class_instance_Mbus.build_chart_act_events()

    def build_saved_events_chart(self):
        self.commands = ""
        self.class_instance_Mbus.build_chart_svd_events()

    def build_dt_flow_chart(self):
        self.commands = ""
        self.class_instance_Mbus.build_ch_dt()


    def read_command(self):
        while True:
            self.commands = raw_input()
            print ("Komenda %r" %self.commands + "\n")

    def cup_class_execute_commands(self):
        if len(self.commands) == 0:
            return None
        # ad_spds-scenarios/MWN250_normal.txt
        elif self.commands[0:7] == 'ad_spds':
            tmp_speed_list = table_of_speeds_from_file(self.commands[8:])
            for element in tmp_speed_list:
                self.class_instance_Cup.test.append(element)
                print("dodaje element %r" %element)
            self.commands = ""
        elif self.commands == "act_speed":
            print("{} Aktualnie uruchomiona predkosc{}".format(date_time_log_file(),self.class_instance_Cup.actual_speed))

    def execute_class_method(self):
        dict_execute_commands = {'ch':self.build_all_charats , 'flw':self.build_flow_chart, 'avg':self.build_avg_speed_chart,
                                      'ae':self.build_actual_events_chart, 'se':self.build_saved_events_chart, 'dt':self.build_dt_flow_chart}
        if self.commands in dict_execute_commands:
            dict_execute_commands[self.commands]()
        elif self.commands == '':
            pass
        else:
            self.cup_class_execute_commands()
            print ("\nNieprawidlowa komenda \n")
            self.commands = ""



    def move_time_boundry(self):
        self.print_after = datetime.datetime.now() + datetime.timedelta(hours=self.print_every)

    def print_on_datetime(self):
        if datetime.datetime.now() > self.print_after:
            self.class_instance_Mbus.build_chart()
            # print ("weszlo")
            self.move_time_boundry()
            self.class_instance_Mbus.dt_flow = []
            self.class_instance_Mbus.x_val_AVG_flow = []
            self.class_instance_Mbus.x_val_all_flow = []
            self.class_instance_Mbus.x_events_saved = []
            self.class_instance_Mbus.x_events_actual = []
            self.class_instance_Mbus.y_date_time = []
        else:
            pass
            # print ("Jeszcze  nie")

if __name__ =="__main__":

    komendy = Commands()
    komendy.print_on_datetime(1)
    time.sleep(7)
    komendy.print_on_datetime(1)
    komendy.print_on_datetime(1)



