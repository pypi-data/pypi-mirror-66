import os

from netmiko import Netmiko
import xlrd
import xlwt

def function_capture(data_dir,capture_path):

    book = xlrd.open_workbook(data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

    for i in range(first_sheet.nrows):
        my_device = {
            "host": first_sheet.row_values(i)[1],
            "username": first_sheet.row_values(i)[2],
            "password": first_sheet.row_values(i)[3],
            "device_type": first_sheet.row_values(i)[4],
        }
        print('Device Executed :')
        print(first_sheet.row_values(i)[0]+' '+my_device["host"])
        write=open(capture_path+'/'+first_sheet.row_values(i)[0]+'-'+first_sheet.row_values(i)[1]+'.txt','w')
        
        try:
            net_connect = Netmiko(**my_device)
            #key information about device
            write.write(first_sheet.row_values(i)[4]+'\n')
            #show ver
            count_column = 5
            while count_column < 105:
                output = net_connect.send_command(first_sheet.row_values(i)[count_column])
                print(output)
                write.write(first_sheet.row_values(i)[count_column]+'\n')
                write.write(output+'\n')
                count_column+=1
            #show run
            '''output = net_connect.send_command(first_sheet.row_values(i)[6])
            print(output)
            write.write(first_sheet.row_values(i)[6]+'\n')
            write.write(output)'''
            #disconnect netmiko
            net_connect.disconnect()
        
        except:
            write.write('Cannot Remote Device')

def function_analyze_capture(files):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Summary')

    count_row = 0
    for i in files:
        try:

            #open file
            read_file = open(i,'r')
            #melakukan read/baca terhadap file
            data = (read_file.read())
            #function nya si ntc_templates, parse_ouput
            parsed_file = parse_output(platform = 'cisco_ios', command = 'show ver', data=data)
            #print(parsed_file)

            #len_file = len(parsed_file)
            #print(len_file)

            list_file = parsed_file[0]
            #print(list_file)

            dic_file_ver = list_file['version']


            dic_file_hw = list_file['hardware']
            file_hw = dic_file_hw[0]
            print(str(count_row)+' '+dic_file_ver+' '+file_hw)
            
            #file name
            ws.write(count_row, 0, i)
            #version
            ws.write(count_row, 1, dic_file_ver)
            #hardware
            ws.write(count_row, 2, file_hw)



        except:
            #file name
            ws.write(count_row, 0, i)
            #version
            ws.write(count_row, 1, 'None')
            #hardware
            ws.write(count_row, 2, 'None')
        count_row+=1

    wb.save('result.xls')