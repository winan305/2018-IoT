import Controller as Controller
from random import *
import time
import threading
#import DBManager

from datetime import datetime
'''
IoT Team Project Source Code - Last update : YYYY-MM-DD (comment if need)
'''

class Game:
    '''
    게임진행 메인 클래스
    1. 게임 준비를 하고
    2. 게임 진행을 하고
    3. 게임 결과를 저장
    4. 게임 내용 초기화
    위 과정 반복.
    ready() -> play() -> save() -> reset() -> ready() -> ...
    위 과정을 run() 에서 실행
    '''

    REQ_TARGET_UP, REQ_TARGET_DOWN = 0, 1
    GAME_MODE_SINGLE = "single"
    GAME_MODE_TEAM = "team"
    GAME_MODE_DEMO = "demo"
    GAME_TIME_LIMIT = 5 # 3sec
    
    def __init__(self, game_mode, game_participants_num, game_participants_name, game_repeat = 10, game_interval = 3):
    
        '''
        파이에 전원 꽂으면 Main 객체가 생성되도록 하고
        컨트롤러 객체 생성해서 컨트롤러 핀 모드 초기화
        그러고나서 게임에 필요한거 초기화하고 run 함수 부르면 될듯
        '''
        print("<Game> - Game Class Object init")
        self.controller = Controller.Controller()
        self.target_number = self.controller.TARGET_NUMBER

        # 게임 모드, 참가자, 라운드 횟수, 라운드간 쉬는 시간
        self.game_mode = game_mode.lower()
        self.game_participants_num = game_participants_num
        self.game_participants_name = game_participants_name
        self.game_repeat = game_repeat
        self.game_interval = game_interval
        
        self.is_clear = False
        self.is_time_over = False
        self.game_round = 0
        print("<Game> - Game init :", self.game_mode, self.game_participants_num, self.game_participants_name)
        
    def ready(self):
        '''
        앱으로 부터 게임모드, 인원수 등을 받았겠지
        그 값들 세팅
        컨트롤러에서 initSensorState 함수 호출
        왜 여기서 이 함수를 호출하냐?
        게임 진행 전 마다 세팅해줘야 그 순간순간 조도값에 맞출 수 있겠지?
        '''
        self.controller.initSensorState()
        print("<Game> - Call ready()")
        pass

    def play(self, game_mode):
        '''
        게임 진행 하는 함수
        '''
        print("<Game> - Call play()")

        if game_mode == self.GAME_MODE_SINGLE :
            return self.play_single()

        elif game_mode == self.GAME_MODE_TEAM :
            return self.play_team(self.game_participants_num)

        elif game_mode == self.GAME_MODE_DEMO :
            self.play_demo()
    
    def time_over(self, round) :
        if round is not self.game_round : return
        if not self.is_clear :
            self.is_time_over = True
            
    def init_state(self) :
        self.is_time_over = False
        self.is_clear = False
    
    def set_fire_timer(self):
        fire_timer = threading.Timer(self.GAME_TIME_LIMIT, self.time_over, args=[self.game_round])
        fire_timer.start()
        
    def play_single(self) :
        '''
        싱글모드.
        표적지를 한 개만 랜덤하게 세움.
        phone_number, play_date, accuracy, max_time, min_time, avg_time
        '''
        game_time = 0
        success_count = 0
        phone_number = self.game_participants_name
        play_date = datetime.now().strftime('%Y%m%d')
        max_time = 0
        min_time = 9876543210

        print("<Game> - Game Mode : Single")
        for repeat in range(self.game_repeat):
            print("<Game> - Game No :", repeat)
            self.game_round = repeat
            self.init_state()
            
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1
            target = randrange(self.target_number)
            light_sensor_head = target*2
            light_sensor_body = target*2+1
            print("<Game> - Target :", target)
            
            self.controller.controllTarget(target, self.REQ_TARGET_UP)
            time.sleep(1)
            self.set_fire_timer()
            start_time = time.time()
            while not self.is_time_over :
                if (self.controller.getLightSensorState(light_sensor_head)
                       or self.controller.getLightSensorState(light_sensor_body)) :
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    game_time += elapsed_time
                    print("<Game> - Clear!")
                    print("<Game> - Elapsed_time :", elapsed_time)
                    self.is_clear = True
                    max_time = max(max_time, elapsed_time)
                    min_time = min(min_time, elapsed_time)
                    success_count += 1
                    break
            
            if not self.is_clear :
                print("<Game> -No Clear!!")
                
            self.controller.controllTarget(target, self.REQ_TARGET_DOWN)
            time.sleep(self.game_interval)
            
        print("<Game> - Single mode finish")
        accuracy = success_count / self.game_repeat
        avg_time = game_time / self.game_repeat
        self.controller.stop()
        game_result = [phone_number, play_date, round(accuracy,2), round(max_time,2), round(min_time,2), round(avg_time,2)]
        return game_result
    
    def play_team(self, game_participants_num):
        '''
        팀모드.
        표적지를 참여자 수 만큼 랜덤하게 세움
        :param game_participant: 참가자 수
        '''
        game_time = 0
        success_count = 0
        team_name = self.game_participants_name
        play_date = datetime.now().strftime('%Y%m%d')
        max_time = 0
        min_time = 9876543210

        print("<Game> - Game Mode : Team")
        for repeat in range(self.game_repeat):
            print("<Game> - Game No :", repeat)
            self.game_round = repeat
            self.init_state()
            # target = randrange(self.TARGET)
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1

            # 0,1,2,3 중에 게임 참가자만큼의 개수를 랜덤한 리스트로 반환함. (3명이면 0,2,3 이런식)
            targets = sample(range(self.target_number), game_participants_num)
            light_sensor_heads = [target*2 for target in targets]
            light_sensor_bodys = [target*2+1 for target in targets]
            print("<Game> - Targets :", targets)
            down_target = []
            for target in targets :
                self.controller.controllTarget(target, self.REQ_TARGET_UP)
            time.sleep(1)
            self.set_fire_timer()
            start_time = time.time()
            while not self.is_time_over :

                for i in range(game_participants_num) :
                    if i in down_target : continue
                    
                    if self.controller.getLightSensorState(light_sensor_heads[i]) :
                        self.controller.controllTarget(targets[i], self.REQ_TARGET_DOWN)
                        down_target.append(i)
                    
                    elif self.controller.getLightSensorState(light_sensor_bodys[i]) :
                        self.controller.controllTarget(targets[i], self.REQ_TARGET_DOWN)
                        down_target.append(i)
                        
                if len(down_target) is game_participants_num :
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    game_time += elapsed_time
                    max_time = max(max_time, elapsed_time)
                    min_time = min(min_time, elapsed_time)
                    success_count += 1
                    print("<Game> - Clear!")
                    print("<Game> - Elapsed_time :", elapsed_time)
                    self.is_clear = True
                    break
                
            if not self.is_clear :
                print("<Game> - No Clear!!")
                
            for target in targets:
                self.controller.controllTarget(target, self.REQ_TARGET_DOWN)

            time.sleep(self.game_interval)
        accuracy = success_count / self.game_repeat
        avg_time = game_time / self.game_repeat
        print("<Game> - Team mode finish")
        self.controller.stop()
        return [team_name, play_date, round(accuracy,2), round(max_time,2), round(min_time,2), round(avg_time,2)]

    def run(self):
        '''
        런~
        '''
        print("<Game> - Call run()")
        self.ready()
        game_result = self.play(self.game_mode) 
        print("<Game> - Game Finish!!")
        return game_result

#game = Game(game_mode="team", game_participants_num=2, game_participants_name="team", game_repeat=5)
#game = Game(game_mode="single", game_participants_num=1, game_participants_name="01082222910", game_repeat=10)
#game.run()

