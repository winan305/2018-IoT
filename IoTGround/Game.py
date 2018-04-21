import Controller as Controller
from random import *
import time
'''
IoT Team Project Source Code - Last update : YYYY-MM-DD (comment if need)
'''

class Game:
    '''
    게임진행 메인 클래스
    1. 게임 요청을 받고
    2. 게임 준비를 하고
    3. 게임 진행을 하고
    4. 게임 결과를 저장
    5. 게임 내용 초기화
    위 과정 반복.
    waitRequest() -> ready2Play() -> play() -> saveResult() -> reset() -> waitRequest() -> ...
    위 과정을 run() 에서 실행
    '''

    REQ_TARGET_UP, REQ_TARGET_DOWN = 0, 1
    GAME_MODE_SINGLE = "single"
    GAME_MODE_TEAM = "team"

    def __init__(self, game_mode, game_participant, game_repeat = 10, game_interval = 3):
        '''
        파이에 전원 꽂으면 Main 객체가 생성되도록 하고
        컨트롤러 객체 생성해서 컨트롤러 핀 모드 초기화
        그러고나서 게임에 필요한거 초기화하고 run 함수 부르면 될듯
        '''
        print("Game Class Object init")
        self.controller = Controller.Controller()
        self.target_number = self.controller.TARGET_NUMBER

        # 게임 모드, 참가자, 라운드 횟수, 라운드간 쉬는 시간
        self.game_mode = game_mode.toLowerCase()
        self.game_participant = game_participant
        self.game_repeat = game_repeat
        self.game_interval = game_interval

        pass

    def wait(self):
        '''
        안드로이드 앱으로부터 요청이 올 때 까지 대기.
        '''
        print("Call waitRequest()")
        pass

    def ready(self):
        '''
        앱으로 부터 게임모드, 인원수 등을 받았겠지
        그 값들 세팅
        컨트롤러에서 initSensorState 함수 호출
        왜 여기서 이 함수를 호출하냐?
        게임 진행 전 마다 세팅해줘야 그 순간순간 조도값에 맞출 수 있겠지?
        '''
        self.controller.initSensorState()
        print("Call ready2play()")
        pass

    def play(self, game_mode):
        '''
        게임 진행 하는 함수지 뭐.
        게임모드, 인원수 맞춰서 표적을 세워야 함
        아마 멀티 쓰레딩이 필요할 듯 싶은데. 흠..
        고민좀 해봐야할듯
        '''
        print("Call play()")

        if game_mode is self.GAME_MODE_SINGLE :
            self.play_single()

        elif game_mode is self.GAME_MODE_TEAM :
            self.play_team(self.game_participant)

        print("Game Finish!!")

    def play_single(self) :
        '''
        싱글모드.
        표적지를 한 개만 랜덤하게 세움.
        '''
        print("Game Mode : Single")
        for repeat in range(self.game_repeat):
            print("Game No :", repeat)
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1
            target = randrange(self.target_number)
            light_sensor_head = target*2
            light_sensor_body = target*2+1

            self.controller.controllTarget(target, self.REQ_TARGET_UP)
            while not (self.controller.getLightSensorState(light_sensor_head)
                       or self.controller.getLightSensorState(light_sensor_body)):
                continue
            self.controller.controllTarget(target, self.REQ_TARGET_DOWN)

            time.sleep(self.game_interval)

    def play_team(self, game_participant):
        '''
        팀모드.
        표적지를 참여자 수 만큼 랜덤하게 세움
        :param game_participant: 참가자 수
        '''
        print("Game Mode : Team")
        for repeat in range(self.game_repeat):
            print("Game No :", repeat)
            # target = randrange(self.TARGET)
            # (target/light_sensor) = (0/0,1) (1/2,3) (2/4,5) (3/6,7)
            # light_sensor = target*2, target*2+1

            # 0,1,2,3 중에 게임 참가자만큼의 개수를 랜덤한 리스트로 반환함. (3명이면 0,2,3 이런식)
            targets = random.sample(range(self.target_number), game_participant)
            light_sensor_heads = [target*2 for target in targets]
            light_sensor_bodys = [head+1 for head in light_sensor_heads]

            down_count = game_participant
            for target in targets :
                self.controller.controllTarget(target, self.REQ_TARGET_UP)

            while down_count > 0 :
                for i in range(game_participant) :
                    if self.controller.getLightSensorState(light_sensor_heads[i]) or self.controller.getLightSensorState(light_sensor_bodys[i]) :
                        self.controller.controllTarget(targets[i], self.REQ_TARGET_DOWN)
                        down_count -= 1

            for target in targets:
                self.controller.controllTarget(target, self.REQ_TARGET_DOWN)

            time.sleep(self.game_interval)

    def save(self):
        '''
        게임 끝나면 결과가 저장되어 있겠지?
        그 값들 데이터베이스에 저장하자.
        '''
        print("Call saveResult()")
        pass

    def reset(self):
        '''
        게임 진행하면서 저장된 값들이 있을 것임.
        그 값들을 초기화 해서 다음 게임에 지장없게.
        '''
        print("Call reset()")
        pass

    def run(self):
        '''
        런~
        '''
        print("Call run()")
        self.wait()
        self.ready()
        self.play(self.game_mode)
        self.save()
        self.reset()
        pass

game = Game(game_mode="single", game_participant=1)
game.run()