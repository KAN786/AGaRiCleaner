

from collections import deque
from transformers import AutoTokenizer, AutoModel
import requests
import time 
from gradio_client import Client

class UserServices:
    honorLevel: int
    messageEvalList: deque[tuple[bool, int]]

    learningRate = 0.1
    bayesianCnt = 50

    def __init__(self, honorLevel: int, messageEvalList: deque[tuple[bool, int]]):
        self.honorLevel = honorLevel
        self.messageEvalList = messageEvalList

    def update_honor(self, evalResult: tuple[bool, int]):
        def calc(x: tuple[bool, int]):
            
            delta = self.learningRate * x[1] * self.honorLevel * (1 - self.honorLevel);
            delta = -delta if x[0] else delta
            self.honorLevel += delta
        
        # 추가
        self.messageEvalList.append(evalResult)
        calc(evalResult)
        

        # 150 넘으면 가장 오래된 메세지 지우기
        if(len(self.messageEvalList) > 150):
            temp = self.messageEvalList.popleft()
            calc((not temp[0], temp[1]))
            
    
    def getBayesianHonorLevel(self, serverAverage) -> float:
        v = len(self.messageEvalList)

        return v / (v + self.bayesianCnt) * self.honorLevel + \
               self.bayesianCnt / (v + self.bayesianCnt) * serverAverage



    def getHonorLevel(self) -> int:
        return self.honorLevel
    
    def getMessageEvalList(self) -> list:
        return self.messageEvalList



class MessageServices:
    
    def __init__(self, client: Client):
        self.client = client
        pass

        

    def get_agaricleaner_result(self, message: str):
        
        result = self.client.predict(
                texts=message,
                api_name="/predict"
        )
        return result
        


if __name__ == "__main__":
    messageServices = MessageServices(Client("CLOUDYUL/AGaRiCleaner_Detector"))

    print("Agaricleaner Result:")
    result = messageServices.get_agaricleaner_result("씨발 존나게 더럽네")
    print(result)

