#using netmiko without raw_data include device_type
import xlrd
import xlsxwriter
from netmiko import Netmiko

def device_identification(raw_data_dir):
    book = xlrd.open_workbook(raw_data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

    wb = xlsxwriter.Workbook('devices_data.xlsx')
    ws = wb.add_worksheet('summary')

    suported_device = ['cisco_ios','cisco_wlc','cisco_xr','cisco_asa','cisco_nxos','cisco_xe']
    count_row = 0

    for i in range(first_sheet.nrows):
        print('Executing Device :')
        print(first_sheet.row_values(i)[0])
        for j in suported_device:

            try:

                my_device = {
                    "host": first_sheet.row_values(i)[1],
                    "username": first_sheet.row_values(i)[2],
                    "password": first_sheet.row_values(i)[3],
                    "device_type": j,
                    "timeout" : 10,
                }

                net_connect = Netmiko(**my_device)
                output = net_connect.send_command('show ver')
                if 'Incorrect' in output:
                    output = net_connect.send_command('show sysinfo')
                print(output)

                ws.write(count_row,0,first_sheet.row_values(i)[0])
                ws.write(count_row,1,my_device["host"])
                ws.write(count_row,2,my_device["username"])
                ws.write(count_row,3,my_device["password"])
                #harus di cari device typenya
                #ws.write(count_row,4,my_device["device_type"])


                if 'Cisco Adaptive Security Appliance Software' in output:                                                   
                    ws.write(count_row,4,'cisco_asa')

                elif 'Cisco IOS XE Software' in output:                                                    
                    ws.write(count_row,4,'cisco_xe')

                elif 'Cisco IOS Software' in output:
                    ws.write(count_row,4,'cisco_ios')                           
                    
                elif 'Cisco Nexus Operating System (NX-OS) Software' in output:                         
                    ws.write(count_row,4,'cisco_nxos')                          
                    
                elif 'Cisco Controller' in output:                         
                    ws.write(count_row,4,'cisco_wlc')
                
                else:
                    ws.write(count_row,4,'unidentified')     


                if 'C3850' in output:
                    ws.write(count_row,5,'C3850')
                    break
                elif 'C2960' in output:
                    ws.write(count_row,5,'C2960')
                    break
                elif 'C9200L' in output:
                    ws.write(count_row,5,'C9200L')
                    break
                elif 'Cisco Controller' in output:
                    ws.write(count_row,5,'Cisco_Controller')
                    break
                elif 'ASA5585' in output:
                    ws.write(count_row,5,'ASA5585')
                    break
                else:
                    ws.write(count_row,5,'unidentified')
                    break   
            
            #except NameError:
                #raise
            except:
                #pass
                my_device = {
                    "host": first_sheet.row_values(i)[1],
                    "username": first_sheet.row_values(i)[2],
                    "password": first_sheet.row_values(i)[3],
                    "device_type": j,
                    "timeout" : 5,
                }

                ws.write(count_row,0,first_sheet.row_values(i)[0])
                ws.write(count_row,1,my_device["host"])
                ws.write(count_row,2,my_device["username"])
                ws.write(count_row,3,my_device["password"])
                ws.write(count_row,4,'-')
                ws.write(count_row,5,'-')
                
        count_row+=1
    wb.close()