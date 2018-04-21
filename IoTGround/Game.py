import Controller as Controller
from random import *
import time

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

    NUM_OF_TARGETS = 4
    REQ_TARGET_UP, REQ_TARGET_DOWN = 0, 1
    def __init__(self):
        '''
        파이에 전원 꽂으면 Main 객체가 생성되도록 하고
        컨트롤러 객체 생성해서 컨트롤러 핀 모드 초기화
        그러고나서 게임에 필요한거 초기화하고 run 함수 부르면 될듯
        '''
        print("Game Class Object init")
        self.controller = Controller.Controller()
        pass

    def waitRequest(self):
        '''
        안드로이드 앱으로부터 요청이 올 때 까지 대기.
        '''
        print("Call waitRequest()")
        pass

    def ready2play(self):
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

    def play(self):
        '''
        게임 진행 하는 함수지 뭐.
        게임모드, 인원수 맞춰서 표적을 세워야 함
        아마 멀티 쓰레딩이 필요할 듯 싶은데. 흠..
        고민좀 해봐야할듯
        '''
        print("Call play()")
        #light_sensor = randrange(self.NUM_OF_TARGETS)
        for repeat in range(5) :
            print("Game No :", repeat)
            time.sleep(3)
            light_sensor = 0
            target = light_sensor//2
            
            self.controller.controllTarget(target, self.REQ_TARGET_UP)
            while not self.controller.getLightSensorState(light_sensor) : continue
            self.controller.controllTarget(target, self.REQ_TARGET_DOWN)
        print("Game Finish!!")
        
    def saveResult(self):
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
        self.waitRequest()
        self.ready2play()
        self.play()
        self.saveResult()
        self.reset()
        pass

game = Game()
game.run()