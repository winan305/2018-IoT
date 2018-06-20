#!
import sqlite3

GAME_MODE_TEAM = 2
GAME_MODE_SOLO = 1

class DBManager :

    def __init__(self):
        self.conn_solo = sqlite3.connect("IoTGround_solo.db")
        self.conn_team = sqlite3.connect("IoTGround_team.db")
        self.cur_solo = self.conn_solo.cursor()
        self.cur_team = self.conn_team.cursor()
        #self.drop_tables()
        self.create_tables()

    def drop_tables(self):
        self.cur_solo.execute('drop table if exists solo')
        self.cur_team.execute('drop table if exists team')

    def create_tables(self):
        sql_solo = "create table IF NOT EXISTS solo" \
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                   "phone_number TEXT, " \
                   "play_date TEXT," \
                   "accuracy REAR," \
                   "max_time REAR," \
                   "min_time REAR," \
                   "avg_time REAR)"


        sql_team = "create table IF NOT EXISTS team" \
                   "(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                   "team_name TEXT, " \
                   "play_date TEXT," \
                   "accuracy REAR," \
                   "max_time REAR," \
                   "min_time REAR," \
                   "avg_time REAR)"

        self.cur_solo.execute(sql_solo)
        self.cur_team.execute(sql_team)

        self.conn_solo.commit()
        self.conn_team.commit()

    def insert_game_result(self, game_result, game_mode):
        if game_mode is GAME_MODE_SOLO :
            sql = "insert into solo(phone_number, play_date, accuracy, max_time, min_time, avg_time) " \
                  "values (?,?,?,?,?,?)"
            self.cur_solo.execute(sql, game_result)
            self.conn_solo.commit()

        elif game_mode is GAME_MODE_TEAM :
            sql = "insert into team(team_name, play_date, accuracy, max_time, min_time, avg_time) " \
                  "values (?,?,?,?,?,?)"
            self.cur_team.execute(sql, game_result)
            self.conn_team.commit()

    def select_results_all(self) :
        cursor = self.cur_solo
        sql = "select * from solo"

        if sql is not None:
            cursor.execute(sql)
            
        print("All result :")

        rows = cursor.fetchall()
        datas = []
        for row in rows :
            data = "/".join(list(map(str, row)))
            datas.append(data)
        for data in datas :
            print(data)
            
    def select_results(self, name, game_mode) :
        cursor = None
        sql = None
        if game_mode is GAME_MODE_SOLO:
            cursor = self.cur_solo
            sql = "select * from solo where phone_number = '" + name + "'"

        elif game_mode is GAME_MODE_TEAM:
            cursor = self.cur_team
            sql = "select * from team where team_name = '" + name + "'"

        if sql is not None:
            cursor.execute(sql)

        rows = cursor.fetchall()
        datas = []
        for row in rows :
            data = "/".join(list(map(str, row)))
            datas.append(data)
        for data in datas :
            print(data)

    def get_ranking_list(self, game_mode) :
        '''
        phone_number, play_date, accuracy, max_time, min_time, avg_time
        기준 : 명중률 > 평균반응속도 > 최소반응속도 > 최대반응속도 > 날짜
        select * from solo
        where phone_number = (select phone_number from solo)
        :return:
        '''
        if game_mode is GAME_MODE_SOLO :
            sql = "select * from solo " \
                  "order by accuracy desc," \
                  "avg_time asc," \
                  "min_time asc," \
                  "max_time asc," \
                  "play_date desc"
            cursor = self.cur_solo
            
        elif game_mode is GAME_MODE_TEAM :
            sql = "select * from team " \
                  "order by accuracy desc," \
                  "avg_time asc," \
                  "min_time asc," \
                  "max_time asc," \
                  "play_date desc"
            cursor = self.cur_team

        cursor.execute(sql)
        rows = cursor.fetchall()
        rankings_dict = {}
        rankings = []
        for row in rows :
            if not row[1] in rankings_dict :
                data = "-".join(list(map(str, row)))
                rankings_dict[row[1]] = data
                rankings.append(data)
                
        print("-".join(rankings))
        return "-".join(rankings)

'''manager = DBManager()
manager.insert_game_result(["01082222910", "20180531", 0.78, 3.51, 2.78, 1.77], GAME_MODE_SOLO)
manager.insert_game_result(["01082222910", "20180531", 0.88, 3.31, 2.11, 1.54], GAME_MODE_SOLO)
manager.insert_game_result(["01082222910", "20180531", 0.91, 2.51, 1.38, 1.21], GAME_MODE_SOLO)
manager.insert_game_result(["01012345678", "20180531", 0.56, 3.51, 2.63, 2.01], GAME_MODE_SOLO)
manager.insert_game_result(["01012345678", "20180531", 0.74, 3.11, 2.13, 1.97], GAME_MODE_SOLO)
manager.insert_game_result(["01012345678", "20180531", 0.77, 1.78, 1.08, 0.98], GAME_MODE_SOLO)
manager.insert_game_result(["01011112222", "20180531", 0.31, 4.15, 3.95, 2.36], GAME_MODE_SOLO)
manager.insert_game_result(["01011112222", "20180531", 0.66, 3.31, 2.97, 2.11], GAME_MODE_SOLO)
manager.insert_game_result(["01011112222", "20180531", 0.97, 2.11, 1.87, 1.54], GAME_MODE_SOLO)'''


#print(manager.get_ranking_list())
#manager.insert_game_result(["ABC", "20180531", 1.23, 2.63, 1.17, 1.81], GAME_MODE_TEAM)
'''manager.select_results("01082222910", GAME_MODE_SOLO)
manager.select_results("01012345678", GAME_MODE_SOLO)
manager.select_results("01011112222", GAME_MODE_SOLO)
manager.select_results("ABC", GAME_MODE_TEAM)'''


