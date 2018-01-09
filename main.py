import time
from threading import Thread
from ClassSerialPort import PortC
from frame_to_Send import ConstructFrame
from console_colours import ConProgress
from comands import Commands
# from statis_functions import StaticMethods

#read all frames Data, Events, Config, Service
def read_all_frames(COM_port_class , build_frame):
    list_to_dics = ['d','e','k','s']
    for key in list_to_dics:
        COM_port_class.write_and_read( build_frame.type_frame_to_read(key) )
        time.sleep(.05)
        COM_port_class.write_and_read( build_frame.generate_read_frame() )
        time.sleep(.05)

def read_data(COM_port_class , build_frame):
    # sleep_time = .05
    sleep_time = 1
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

def complete_create_cgart(COM_port_class, temp):
    if temp == 'k':
        COM_port_class.build_chart()


port = "COM20"
frameC = ConstructFrame('30/03/18 23:59', 0x02)
#region Old
frame2 = '\x10\x7B\x0A\x85\x16'
frame3 = '\x10\x5B\x0A\x65\x16'
SND = '\x68\x04\x04\x68\x53\x0A\x50\x02\xA5\x16'
SND2 = '\x68\x09\x09\x68\x73\x0A\x51\x04\x6D\x3A\37\x3E\x2B\x19\x16'
SND3 = '\x68\x09\x09\x68\x53\x0A\x51\x04\x6D\x24\x22\x24\x2C\xB5\x16'
#endregion

if __name__ == '__main__':
    try:
        dostepDoPortu = PortC( port , baud=9600 )
    except:
        print("Brak dostepu do portu")

    command =  Commands(dostepDoPortu)
    thread  = Thread( target=command.read_command )
    thread.start()

    x=0
    steps_ = 10
    send = False
    progress = ConProgress(steps_)
    while x < steps_:
    # while True:

        # dostepDoPortu.write_and_read( frameC.build_wild_card() )
        # change_baudurate(dostepDoPortu , frameC)
        # time.sleep(1)
        #

        # read_data(dostepDoPortu , frameC)
        # command.execute_class_method(dostepDoPortu)

        # look_for_cup_on_evry_baudurate(dostepDoPortu , frameC)

        # read_all_frames(dostepDoPortu , frameC)

        get_back_from_test_mode(dostepDoPortu , frameC)
        # get_back_from_test_mode(dostepDoPortu , frameC)
        progress.progress(x)
        x+=1


    # dostepDoPortu.build_chart()
    dostepDoPortu.returnTable()
    print 'Tablica %r' %dostepDoPortu.table
    dostepDoPortu.close()

