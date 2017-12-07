from functools import reduce
from statis_functions import StaticMethods




class ConstructFrame(object):


    def __init__(self , start_time, adressDEC):
        #region Building frames
        self.firsForth      = 0x68
        self.length         = 0x09
        self.adress         = int(adressDEC)
        self.new_adress     = 10
        self.hours          = int(start_time[9:11])
        self.minutes        = int(start_time[12:14])
        self.year           = int(start_time[6:8])
        self.month          = int(start_time[3:5])
        self.day            = int(start_time[0:2])
        self.lastByte       = 0x16
        #endregion

        #region manipulating with wildcard
        self.client_number_4B = [0xFF,0xFF,0xFF,0xFF]
        self.manufacture    = [0xFF,0xFF]
        self.version        = 0xFF
        self.medium         = 0xFF
        #endregion

        self.manipulate_crc = True
        self.header = []
        print "{}/{}/{} {}:{}".format(self.day, self.month,self.year,self.hours,self.minutes)

    def construct_frame_Time(self):
        self.header = [self.firsForth , self.length, self.length, self.firsForth , 0x53, self.adress, 0x51,0x04,  0x6D]

    def construct_frame_Update_adress(self):
        self.header = [self.firsForth , 0x06, 0x06, self.firsForth , 0x53, self.adress, 0x51, 0x01,  0x7A]

    def construct_frame_wild_card(self):
        self.header = [self.firsForth , 0x0B, 0x0B, self.firsForth , 0x53, 0xFD, 0x52]

    def construct_frame_to_read_type(self):
        self.header = [self.firsForth, 0x04, 0x04, self.firsForth, 0x73, self.adress, 0x50]

    def crc_and_end(self):
        self.header.append(self.crcCheck(right_crc=self.manipulate_crc))
        self.header.append(0x16)

    def miesiacB4(self):
        tempMiesiac_b4 = self.month
        tempYear_b4 = (self.year & 0x78) << 1
        caly_bajt = tempMiesiac_b4 + tempYear_b4
        # print("%r" % hex(caly_bajt))
        return caly_bajt

    def dzienRokB3(self):
        tmpDzien = self.day
        tmpRok = (self.year & 0x07) << 5
        caly_bajt = tmpDzien + tmpRok
        # print("%r" % hex(caly_bajt))
        return caly_bajt

    def godzWIzB2(self):
        iZW1w0 = 0x20
        temp = self.hours
        caly_bajt = iZW1w0 + temp
        # print("%r" % hex(caly_bajt))
        return caly_bajt

    def min_RWB1(self):
        temp_minutes    = self.minutes & 0x3F
        caly_bajt       = temp_minutes
        # print("%r" % hex(caly_bajt))
        return caly_bajt

    def wywolanie(self):
        self.miesiacB4()
        self.godzWIzB2()
        self.dzienRokB3()
        self.miesiacB4()

    def crcCheck(self, right_crc):
        tempTable = self.header[4:]
        # print "%r" %self.header[4:]
        if right_crc and len(self.header) > 3:
            return reduce(lambda a, b: (a + b) & 0xFF, tempTable, 0)
        elif right_crc == False and len(self.header) > 3:
            return reduce(lambda a, b: (a + b) & 0xFA, tempTable, 0)
        else:
            print( "CRC krotkiego zapytania")
            return reduce(lambda a, b: (a + b) & 0xFF, self.header[1:4], 0)

    def frameToSenD(self):
        frame = ''
        for element in self.header:
            frame += chr(element)
        # print "%r" %frame
        self.header = []
        return frame

    def checkFebruary(self):
        if self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0:
            return 29
        else:
            return 28

    def checkMonth(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year +=1


    def updatimgTime(self):
        daysInMonthDics = {1: 31, 2: self.checkFebruary(), 3:31, 4:30, 5:31 , 6:30, 7:30, 8:31, 9:30, 10:31, 11:30, 12:31}
        # print daysInMonthDics[2]
        if daysInMonthDics[self.month] > self.day:
            self.day += 1
        else:
            self.day = 1
            self.checkMonth()
        # print "{}/{}/{} {}:{}".format(self.day, self.month,self.year,self.hours,self.minutes)

    def build_timeupdate_frame(self):
        self.construct_frame_Time()
        self.header.append(self.min_RWB1())
        self.header.append(self.godzWIzB2())
        self.header.append(self.dzienRokB3())
        self.header.append(self.miesiacB4())
        self.header.append(self.crcCheck(self.manipulate_crc))
        self.header.append(0x16)
        # print "%r" %self.header
        print "%r" %" ".join(format(byteInt, '02x') for byteInt in self.header)
        toReturn = self.frameToSenD()
        self.updatimgTime()
        return toReturn

    def build_adresupdate_frame(self):
        self.construct_frame_Update_adress()
        self.header.append(self.new_adress)
        self.header.append(self.crcCheck(self.manipulate_crc))
        self.header.append(0x16)
        temp_returned = self.frameToSenD()
        self.adress = self.new_adress
        if self.new_adress < 251:
            self.new_adress += 1
        else:
            self.new_adress = 0
        return  temp_returned

    def build_wild_card(self):
        self.construct_frame_wild_card()
        for client_num in self.client_number_4B:
            self.header.append(client_num)
        for manu in self.manufacture:
            self.header.append(manu)
        self.header.append(self.version)
        self.header.append(self.medium)
        self.header.append(self.crcCheck(self.manipulate_crc))
        self.header.append(0x16)
        temp_returned = self.frameToSenD()
        # print "%r" %" ".join(format(byteInt, '02x') for byteInt in self.header).upper()
        return  temp_returned

    # get back from test mode to normal mode
    def get_bact_to_normale_state(self):
        temp_list = [0x02,0x05,0x43,0x7F,0x03]
        temp_lisst_to_send = StaticMethods.create_frame(temp_list)
        # print "%r" %" ".join(format(byteInt, '02x') for byteInt in temp_list).upper()
        return temp_lisst_to_send

    # 68 04 04 68 73 00 50 00 C3 16
    # choose which frame do u want to read
    def type_frame_to_read(self , frame_type):
        # dict_frame = {'data' : 0x00, 'events': 0x01, 'konf': 0x02, 'service': 0x03 }
        dict_frame = {'d' : 0x00, 'e': 0x01, 'k': 0x02, 's': 0x03 }
        self.construct_frame_to_read_type()
        self.header.append( dict_frame[frame_type] )
        self.crc_and_end()
        temp_return = self.frameToSenD()
        # print "%r" %" ".join(format(byteInt, '02x') for byteInt in temp_return).upper()
        return temp_return

    # read data from device
    def generate_read_frame(self):
        self.header = [0x10, 0x7B, self.adress]
        self.crc_and_end()
        temp_return = self.frameToSenD()
        # print "%r" %" ".join(format(byteInt, '02x') for byteInt in temp_return).upper()
        return temp_return

    def change_baudurate(self, rate=2400):
        self.header = [self.firsForth, 0x03, 0x03, self.firsForth, 0x73, self.adress]
        if rate == 2400:
            self.header.append(0xBB)
            self.crc_and_end()
        elif rate == 9600:
            self.header.append(0xBD)
            self.crc_and_end()
        elif rate == 300:
            self.header.append(0xB8)
            self.crc_and_end()
        # print "%r" %" ".join(format(byteInt, '02x') for byteInt in self.header).upper()
        temp_return = self.frameToSenD()
        return temp_return



# 68 09 09 68   73 0A 51 04 6D 3A 37 3E 2B  19 16

if __name__ == '__main__':

    chartemp = "01/01/17 23:59"

    x = ConstructFrame(chartemp, 4)

    # x.wywolanie()
    #
    # x.buildFrame()
    # x.buildFrame()
    # x.buildFrame()
    # x.build_wild_card()
    # x.generate_read_frame()
    x.change_baudurate('24')
    # for i in range(365):
    #     x.updatimgTime()
