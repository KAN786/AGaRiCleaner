

from collections import deque



class User:
    id: int
    honorLevel: int
    messageEvalList: deque[tuple[bool, int]]

    learningRate = 0.1
    bayesianCnt = 50

    def __init__(self, id: int, honorLevel: int, messageEvalList: deque[tuple[bool, int]]):
        self.id = id
        self.honorLevel = honorLevel
        self.messageEvalList = messageEvalList

    def update_honor(self, evalResult: tuple[bool, int]):
        def calc(x: tuple[bool, int]):
            
            delta = self.learningRate * x[1] * self.honorLevel * (1 - self.honorLevel);
            delta = delta if x[1] else -delta
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



    def getId(self) -> int:
        return self.id
    
    def getHonorLevel(self) -> int:
        return self.honorLevel
    
    def getMessageEvalList(self) -> list:
        return self.messageEvalList


    

