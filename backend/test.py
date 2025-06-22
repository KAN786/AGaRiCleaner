import json
import requests
import time  # 너무 빠른 요청 방지용 (선택)

# JSON 파일 로드
with open("teststatements.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 응답 결과 저장할 리스트
responses = []

system_id = "test1"
server_id = "test1"

# API URL
url = f'https://agaricleaner.onrender.com/users/{server_id}/{system_id}'

# 요청 전송
for item in data["comments"]:
    message = item["text"]
    try:
        res = requests.post(url, json={"message": message})
        result = res.json()
    except Exception as e:
        result = {"error": str(e)}
    
    responses.append({
        "text": message,
        "label": item["label"],
        "score": result["score"],
        "is_toxic": result["is_toxic"],
        "honor_level": result["honor_level"]
    })
    
    time.sleep(0.1)  # 서버 과부하 방지를 위한 잠깐 대기 (선택)
    

# 결과 저장
with open("responses_with_labels.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)
