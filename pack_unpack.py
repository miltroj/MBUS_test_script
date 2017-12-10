
def byte_to_little_edian(byte):
    x = byte
    x_8 = (x & 0b00000001)<< 7
    x_7 = (x & 0b00000010)<< 5
    x_6 = (x & 0b00000100)<< 3
    x_5 = (x & 0b00001000)<< 1
    x_4 = (x & 0b00010000)>> 1
    x_3 = (x & 0b00100000)>> 3
    x_2 = (x & 0b01000000)>> 5
    x_1 = (x & 0b10000000)>> 7
    return x_8 + x_7 +x_6 + x_5 + x_4 +x_3 + x_2 + x_1

def bytes_to_lit_edian(frame, first_element):
    return byte_to_little_edian( frame[first_element]), byte_to_little_edian( frame[first_element+1]), byte_to_little_edian( frame[first_element+2])

def parse_events_to_table(element,i,frame):
    temp_first_byte = i + 3
    temp_byte_table = []
    if element is 0x03 and frame[i + 1] is 0xFD and frame[i + 2] is 0x17:
        temp_byte_1,temp_byte_2, temp_byte_3 = bytes_to_lit_edian( frame, temp_first_byte )
        to_convert = (temp_byte_1 << 16) + (temp_byte_2 << 8) + temp_byte_3
        # print("%r" %to_convert)
        # print("B1 %r" %temp_byte_1)
        # print("B1 przes %r" %(temp_byte_1 << 16))
        # print("B2 przes %r" %(temp_byte_2 << 8))
        # print("B3 przes %r" %(temp_byte_3))
        for power in range(23, -1, -1):
            temp_compare = 2 ** power
            if temp_compare == (to_convert & temp_compare):
                temp_byte_table.append(1)
            else:
                temp_byte_table.append(0)
        return temp_byte_table, False
    else:
        return None, True

def iterate_and_find(frame):
    atarms_exist = True
    tablica = []
    if type(frame) == int or frame == None:
        return None
    for i,element in enumerate(frame):
        if atarms_exist:
            tablica, atarms_exist = parse_events_to_table(element,i,frame)
        else:
            break
    return tablica

# for power in range(23,-1,-1):
#     temp_compare = 2**power
#     if temp_compare == (0x800000 & temp_compare):
#         print("E %r"%power)
#         print("E compare %r"%temp_compare)
# # print ("%r" %hex(y))


string = '68 56 56 68 08 04 72 00 00 00 00 01 06 15 07 26 88 00 00 0C 78 00 00 00 00 04 6D 36 A9 21 2C 04 16 FB 00 00 00 02 3E 5A 00 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 67 16'
string_pra = '68 56 56 68 08 04 72 00 00 00 00 01 06 15 07 91 98 00 00 0C 78 00 00 00 00 04 6D 2B AE 27 2C 04 16 C9 0E 00 00 02 3E 00 00 44 16 6A 04 00 00 42 6C 22 2C 02 27 07 00 03 FD 17 85 02 00 04 FF 0A 04 02 01 00 02 FF 0B 00 00 03 FF 0C 51 00 A8 0F 00 07 04 09 FF 00 00 00 00 00 F7 16'


string_probny = '03 FD 17 FF FF FF 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 67 16'
string2 = '68 56 56 68 08 04 72 00 00 00 00 01 06 15 07 26 88 00 00 0C 78 00 00 00 00 04 6D 36 A9 21 2C 04 16 FF FF FF FF 02 3E FF FF 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 67 16'
string3 = '2C 04 11 FF FF FF FF 02 31 FF FF 44 16 00 00 00 00 42 6C 00 00 02 27 01 00 03 FD 17 04 02 00 04 FF 0A 03 02 00 00 02 FF 0B 00 00 03 FF 0C 03 00 A8 0F 00 05 01 09 04 00 00 00 00 00 04 16'
table = string_pra.split(" ")
table_int = [int(element,16) for element in table]

tablica_wyjsciowa = []

tablica_wyjsciowa = iterate_and_find(table_int)

print("%r" %tablica_wyjsciowa)
print("%r" %len(tablica_wyjsciowa))

# print("byte to little edian %r" %byte_to_little_edian(0xFF))

