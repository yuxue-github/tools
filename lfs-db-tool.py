
import pymysql

class LfsDB:
    def __init__(self):
        self.con = None
        self.cursor = None

    def __update_system_releases(self):
        updateSQL = "update system_releases set system_release_name='{0}' where system_release_name='{1}'"
        values = [('FSM-r5', 'SM-r5'), ('AirScale5g5', 'SM-r5_5G'), ('SM6', 'SM-r6')]
        for value in values:
            sql = updateSQL.format(value[1], value[0])
            if (self.cursor.execute(sql) > 0):
                print("executed '" + sql + "' successfully")
        self.con.commit()
        updateSQL = "update system_releases set status='{0}' where system_release_name='{1}'"
        sql = updateSQL.format('closed', 'Lionfish')
        if (self.cursor.execute(sql) > 0):
            print("executed '" + sql + "' successfully")
        self.con.commit()

    def __update_module_types_system_id(self):
        updateSQL = "update module_types set system_release_id='{0}' where module_type='{1}'"
        values = [('fcmd_fspc', 2), ('FCTM_ASPB', 4), ('host', 7), ('ASCB', 11),
                    ('FCTJ_FSMF', 4), ('FCTM_FSMF', 4), ('sm-r5_5g', 11), ('sm-r6', 13),
                    ('sm-r5-nocmem', 5), ('sm-r5', 5), ('fsm4_axm64', 4)]
        for value in values:
            sql = updateSQL.format(value[1], value[0])
            if (self.cursor.execute(sql) > 0):
                print("executed '" + sql + "' successfully")
        self.con.commit()

    def __summarize_by_module_type(self):
        #pass
        self.cursor.execute("select b.module_type, count(*) as num from build_events a \
             inner join module_types b on a.module_type_id = b.id group by a.module_type_id order by num DESC")
        print("(module_type | build_times)")
        for row in self.cursor:
            print(row)

    def start(self):
        self.con = pymysql.connect(host='ulegcpcisand.emea.nsn-net.net', user='lfspt', 
            password = '4ObryufezAm_', database = 'test_lfspt', port = 3306)
        self.cursor = self.con.cursor()
        try:
            self.__summarize_by_module_type()
            self.__update_system_releases()
            self.__update_module_types_system_id()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            self.con.close()

if __name__ == '__main__':
    db = LfsDB()
    db.start()

