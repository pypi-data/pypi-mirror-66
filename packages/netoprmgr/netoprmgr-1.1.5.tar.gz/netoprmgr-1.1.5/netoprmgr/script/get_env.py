import sqlite3
from netoprmgr.device_templates.show_env.env_C3850 import env_C3850
from netoprmgr.device_templates.show_env.env_C2960 import env_C2960
from netoprmgr.device_templates.show_env.env_C2960L import env_C2960L
from netoprmgr.device_templates.show_env.env_C2960X import env_C2960X
from netoprmgr.device_templates.show_env.env_C3650 import env_C3650
from netoprmgr.device_templates.show_env.env_C3750 import env_C3750
from netoprmgr.device_templates.show_env.env_C3750E import env_C3750E
from netoprmgr.device_templates.show_env.env_C3750X import env_C3750X
from netoprmgr.device_templates.show_env.env_C9200L import env_C9200L
from netoprmgr.device_templates.show_env.env_C9300 import env_C9300
from netoprmgr.device_templates.show_env.env_C4507R import env_C4507R


class get_env:
    def __init__(self,files):
        self.files=files

    def get_env(self):
        #destroy table summarytable
        try:
            db = sqlite3.connect('env_pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE envtable''')
            db.commit()
            db.close()
        except:
            pass
        #open db connection to table summary table
        try:
            db = sqlite3.connect('env_pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE envtable(id INTEGER PRIMARY KEY, devicename TEXT,
                                system TEXT, item TEXT, status TEXT)
            ''')
            db.close()
        except:
            pass

        for file in self.files:
            try:
                print('Processing File :')
                print(file)
                read_file = open(file, 'r')
                read_file_list = read_file.readlines()
                #len(read_file_list)
                for i in read_file_list:
                    if 'C3850' in i:
                        env_C3850(file)
                        break
                    elif 'C2960L' in i:
                        env_C2960L(file)
                        break
                    elif 'C2960X' in i:
                        env_C2960X(file)
                        break
                    elif 'C2960' in i:
                        env_C2960(file)
                        break
                    elif 'C3650' in i:
                        env_C3650(file)
                        break
                    elif 'C3750' in i:
                        env_C3750E(file)
                        break
                    elif 'C3750E' in i:
                        env_C3750E(file)
                        break
                    elif 'C3750X' in i:
                        env_C3750X(file)
                        break
                    elif 'C9200L' in i:
                        env_C9200L(file)
                        break
                    elif 'C9300' in i:
                        env_C9300(file)
                        break
                    elif 'C4507R' in i:
                        env_C4507R(file)
                        break

            #except NameError:
            # raise
            except:
                pass
