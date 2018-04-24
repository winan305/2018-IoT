import Game
'''
서버 소스 코드(사실은 MQTT 클라이언트임)
모바일로부터 발송된 MQTT 메세지를 구독해서 처리함.

서버 객체 생성 -> MQTT 클라이언트 생성 및 연결 -> loop_forever -> 요청받으면 요청에 따라 처리 

메세지 프로토콜부터 결정하자.
안드로이드 앱 to 서버 :
 - 전송할 요청 : 게임할래, 내 정보 보여줘, 랭킹 보여줘
 - 받을 데이터/ 보낼 데이터 :
    1. 게임할래 : 없음 / 게임모드, 인원수
    2. 내 정보 보여줘 : 내 아이디에 맞는 정보들 / 없음
    3. 랭킹 보여줘 : 랭킹정보 / 없음

서버 to 안드로이드 앱 :
 - 받을 요청 : 게임할래, 내 정보 보여줘, 랭킹 보여줘
 - 받을 데이터/ 보낼 데이터 :
    1. 게임할래 : 게임모드, 인원수 / 없음
    2. 내 정보 보여줘 : 아이디 / 아이디에 맞는 정보들(게임횟수, 평균 맞춘횟수, 평균 걸린시간 등등)
    3. 랭킹 보여줘 : 아이디 / 아이디에 맞는 정보들(개인랭킹, 모든 랭킹들 등등)
    
    - 요청 : REQ_GAME_PLAY, REQ_GET_INFO, REQ_GET_RANK
    - 결과 : RES_GAME_PLAY, RES_GET_INFO, RES_GET_RANK
    - 데이터 : mode, number ...
'''

class Server :

    def __init__(self):
        print("Server : init Server!")
  
    def start_game(self, data):
        print("Server : start game, Data :",data)
        game_mode, game_participant = data[0], int(data[1])
        game = Game.Game(game_mode=game_mode, game_participant=game_participant)
        game.run()

    def send_user_info(self, data):
        print("Server : send user info, Data :", data)
        return None

    def send_ranking(self, data):
        print("Server : send_ranking, Data :", data)
        return None