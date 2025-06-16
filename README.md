# AGaRiCleaner
AI 기반의 실시간 채팅 필터링 시스템입니다. 명예도 기반의 확률적 메시지 필터링을 통해 유해 발언을 효과적으로 제어합니다.

## 주요 기능
- ai/키워드 기반 메시지 평가
- FastAPI + SQLite 기반 REST API
- 사용자별 통계 제공


## 설치 방법
```bash
git clone https://github.com/yourusername/project-name.git
cd project-name
pip install -r requirements.txt
uvicorn main:app --reload
```

## 사용 예시
input:
```
bash
curl -X POST http://localhost:8000/server1/system3 \
     -H "Content-Type: application/json" \
     -d '{"message": "You suck"}'
```
output:
```
{
  "filtered": true,
  "score": 0.85,
  "label": "toxic"
}
```

## 기여 방법
- Issue를 먼저 생성해 변경 사항을 제안해주세요.
- 이미 유사한 Issue나 PR이 존재하는지 확인해주세요.
- 새로운 기능/버그 수정에는 단위 테스트를 함께 포함시켜주세요.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다. 자유롭게 사용/배포/수정이 가능합니다.

