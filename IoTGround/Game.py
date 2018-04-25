import Controller as Controller
from random import *
import time
import threading
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
    GAME_TIME_LIMIT = 3 # 3sec
    
    def __init__(self, game_mode, game_participant, game_repeat = 10, game_interval = 3):
        '''
        파이에 전원 꽂으면 Main 객체가 생성되도록 하고
        컨트롤러 객체 생성해서 컨트롤러 핀 모드 초기화
        그러고나서 게임에 필요한거 초기화하고 run 함수 부르면 될듯
        '''
        print("Log : Game Class Object init")
        self.controller = Controller.Controller()
        self.target_number = self.controller.TARGET_NUMBER

        # 게임 모드, 참가자, 라운드 횟수, 라운드간 쉬는 시간
        self.game_mode = game_mode.lower()
        self.game_participant = game_participant
        self.game_repeat = game_repeat
        self.game_interval = game_interval
        
        self.is_clear = False
        self.is_time_over = False
        
    def ready(self):
        '''
        앱으로 부터 게임모드, 인원수 등을 받았겠지
        그 값들 세팅
        컨트롤러에서 initSensorState 함수 호출
        왜 여기서 이 함수를 호출하냐?
        게임 진행 전 마다 세팅해줘야 그 순간순간 조도값에 맞출 수 있겠지?
        '''
        self.controller.initSensorState()
        print("Log : Call ready()")
        pass

    def play(self, game_mode):
        '''
        게임 진행 하는 함수지 뭐.
        게임모드, 인원수 맞춰서 표적을 세워야 함
        아마 멀티 쓰레딩이 필요할 듯 싶은데. 흠..
        고민좀 해봐야할듯
        '''
        print("Log : Call play()")

        if game_mode == self.GAME_MODE_SINGLE :
            self.play_single()

        elif game_mode == self.GAME_MODE_TEAM :
            self.play_team(self.game_participant)

        print("Game Finish!!")
    
    def time_over(self) :
        if not self.is_clear :
            self.is_time_over = True
            
    def init_state(self) :
        self.is_time_over = False
        self.is_clear = False
    
    def set_fire_timer(self):
        fire_timer = threading.Timer(self.GAME_TIME_LIMIT, self.time_over, args=[])
        fire_timer.start()
        
    def play_single(self) :
        '''
        싱글모드.
        표적지를 한 개만 랜덤하게 세움.
        '''
        game_time = 0
        
        print("Log : Game Mode : Single")
        for repeat in range(self.game_repeat):
            print("Log : Game No :", repeat)
            self.init_state()
            
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1
            target = randrange(self.target_number)
            light_sensor_head = target*2
            light_sensor_body = target*2+1
            print("Target :", target)
            
            self.controller.controllTarget(target, self.REQ_TARGET_UP)
            
            self.set_fire_timer()
            start_time = time.time()
            while not self.is_time_over :
                if (self.controller.getLightSensorState(light_sensor_head)
                       or self.controller.getLightSensorState(light_sensor_body)) :
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    game_time += elapsed_time
                    print("Log : Clear!")
                    print("Log : Elapsed_time :", elapsed_time)
                    self.is_clear = True
                    break
            
            if not self.is_clear :
                print("Log : No Clear!!")
                
            self.controller.controllTarget(target, self.REQ_TARGET_DOWN)
            time.sleep(self.game_interval)

    def play_team(self, game_participant):
        '''
        팀모드.
        표적지를 참여자 수 만큼 랜덤하게 세움
        :param game_participant: 참가자 수
        '''
        game_time = 0
        print("Log : Game Mode : Team")
        for repeat in range(self.game_repeat):
            print("Log : Game No :", repeat)
            self.init_state()
            # target = randrange(self.TARGET)
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1

            # 0,1,2,3 중에 게임 참가자만큼의 개수를 랜덤한 리스트로 반환함. (3명이면 0,2,3 이런식)
            targets = sample(range(self.target_number), game_participant)
            light_sensor_heads = [target*2 for target in targets]
            light_sensor_bodys = [head+1 for head in light_sensor_heads]
            print("Targets :", targets)
            down_count = game_participant
            
            for target in targets :
                self.controller.controllTarget(target, self.REQ_TARGET_UP)
            
            self.set_fire_timer()
            start_time = time.time()
            while not self.is_time_over :

                for i in range(game_participant) :
                    if (self.controller.getLightSensorState(light_sensor_heads[i])
                    or self.controller.getLightSensorState(light_sensor_bodys[i])) :
                        self.controller.controllTarget(targets[i], self.REQ_TARGET_DOWN)
                        print("Log : Hit!!")
                        down_count -= 1
                        
                if down_count == 0 :
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    game_time += elapsed_time
                    print("Log : Clear!")
                    print("Log : Elapsed_time :", elapsed_time)
                    self.is_clear = True
                    break
                
            if not self.is_clear :
                print("Log : No Clear!!")
                
            for target in targets:
                self.controller.controllTarget(target, self.REQ_TARGET_DOWN)

            time.sleep(self.game_interval)

    def save(self):
        '''
        게임 끝나면 결과가 저장되어 있겠지?
        그 값들 데이터베이스에 저장하자.
        '''
        print("Log : Call save()")

    def reset(self):
        '''
        게임 진행하면서 저장된 값들이 있을 것임.
        그 값들을 초기화 해서 다음 게임에 지장없게.
        '''
        print("Log : Call reset()")
        self.controller.stop()

    def run(self):
        '''
        런~
        '''
        print("Log : Call run()")
        self.ready()
        self.play(self.game_mode)
        self.save()
        self.reset()
    
    def clear(self) :
        '''
        target clear function
        '''
        pass

#game = Game(game_mode="team", game_participant=2, game_repeat=10)
#game.run()