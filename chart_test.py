import time
from threading import Thread
from ClassSerialPort import PortC
from frame_to_Send import ConstructFrame
from console_colours import ConProgress
from comands import Commands
from serial_cup_tester import Cup_tester
from additional_methods import *

def read_all_frames(COM_port_class , build_frame):
    list_to_dics = ['d','e','k','s']
    for key in list_to_dics:
        COM_port_class.write_and_read( build_frame.type_frame_to_read(key) )
        time.sleep(.05)
        COM_port_class.write_and_read( build_frame.generate_read_frame() )
        time.sleep(.05)

def read_data(COM_port_class , build_frame):
    # sleep_time = .05
    sleep_time = 5
    temp_use_once = True
    if temp_use_once:
        COM_port_class.write_and_read( build_frame.type_frame_to_read('d') )
        temp_use_once = False
        time.sleep( sleep_time )
    COM_port_class.write_and_read(build_frame.generate_read_frame())
    time.sleep( sleep_time )

def get_back_from_test_mode(COM_port_class , build_frame):
    COM_port_class.write_and_read( build_frame.get_bact_to_normale_state() )
    COM_port_class.reinit_COM_port(2400)

def change_baudurate(COM_port_class , build_frame):
    baudurate_table = [300,2400,9600]
    for i, baudu in enumerate(baudurate_table):
        print("{} baudurate {}".format(i,baudu))
        COM_port_class.write_and_read_baudurate( build_frame.change_baudurate(baudu), baudu )
        COM_port_class.reinit_COM_port(baudu)
        time.sleep(.5)

def look_for_cup_on_evry_baudurate(COM_port_class , build_frame):
    baudurate_table = [300,2400,9600]
    for i, baudu in enumerate(baudurate_table):
        print("{} baudurate {}".format(i,baudu))
        COM_port_class.reinit_COM_port(baudu)
        time.sleep(.5)
        COM_port_class.write_and_read( build_frame.build_wild_card() )
        time.sleep(.5)

#region Test cases

test_cases_1 = [[0,15],[0.04,15],[0.1,2],[1,1],[3,1],[1,1],[4,1],[8,1],[0,1],[6,2],[7,2],[8,2],[0,60],[-4,30],[0,100],[12,50],[12.7,45],[13,20],[0,10],[-2,10],[10,15]]
test_cases_2 = [[0,15],[5,450]]
test_cases_zero = [[0.04,10]]
test_cases_MWN250 = [[0,1000],[0.02,1500],[0.05,500],[0.08,500],[0.1,500],[0.12,500],[0.14,500],[0.15,500],[0.18,500],[0.19,500],
                     [0.21,500],[0.25,500],[0.277,500],[0.3,500],[0.34,500],[0.35,500],[0.4,500],[-0.15,500],[0,500],[1,500],[2,500],
                     [3,500],[4,500],[5,500],[6,500],[7,500],[0,1000]]

test_cases_MWN250_bledy_wskazowki = [[0,100],[0.44,100],[1,100],[2,100],[-0.5,50],[0,100],[2,50],[-2,50],[0,100]]

test_cases_JS16_MasterC = [[0,100],[0.02,1500],[0.05,500],[0.08,500],[0.1,500],[0.15,500],[0.2,500],[0.25,500],[0,500],[0.30,500],
                     [0.35,500],[0.40,500],[0,500],[0.3,500],[0.34,500],[0.35,500],[0.4,500],[-0.15,500],[0,500],[0.5,500]]

test_cases_JS16_MasterC_wskazowki = [[0,100],[0.05,20],[0.1,20],[0.15,50],[0.2,50],[0.25,50],[0,50],[0.44,120],[0.34,10],
                     [-0.15,50],[0,500],[0.55,50],[0,10]]
# test_cases = [[0,500],[2,1000],[0,1100],[0.04,1000],[0.9,500],[0,2000],[12,500],[0,2000],[12.7,500],[0,2000],
#               [-4,600],[0,2000],[0.02,1000],[0.04,500],[13.7,500],[0.02,1000],[14.7,500],[0.02,1000],[1,1],[2,1],[3,1],[10,1],[0,1000]]

#endregion

speeds_from_file = table_of_speeds_from_file("scenarios/MWN250_normal.txt")
cup_port = 'COM19'
cup_tester = Cup_tester(cup_port,speeds_from_file)
port = "COM20"
frameC = ConstructFrame('30/03/18 23:59', 0x04)

cup_tester.unloop_cup_test = True

steps_ = 73125
sleep_time = 5
send = False
temp_use_once = True


if __name__ == '__main__':
    try:
        dostepDoPortu = PortC( port , baud=9600 )
    except:
        print("Brak dostepu do portu")

    thread_cup = Thread( target=cup_tester.while_write )
    thread_cup.start()

    command =  Commands(dostepDoPortu , cup_tester)
    thread  = Thread( target=command.read_command )
    thread.start()

    progress = ConProgress(steps_)
    while True:
        if temp_use_once:
            dostepDoPortu.write_and_read(frameC.type_frame_to_read('d'))
            temp_use_once = False
            time.sleep(sleep_time)
        dostepDoPortu.write_and_read(frameC.generate_read_frame())
        time.sleep(sleep_time)

        command.execute_class_method()
        command.print_on_datetime()


    print 'Tablica %r' %dostepDoPortu.table
    dostepDoPortu.close()

