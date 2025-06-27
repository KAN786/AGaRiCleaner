# AGaRiCleaner
AI 기반의 실시간 채팅 필터링 시스템입니다. 명예도 기반의 확률적 메시지 필터링을 통해 유해 발언을 효과적으로 제어합니다.

## Contributors
- KAN786 (강대한)
- daehan (강대한)
- m1ntree (황민)

daehan계정은 KAN786과 동일 인물이지만, vscode와 github 계정 연동 문제로 github에서는 KAN786과 개별인물로 표시되었습니다.
또한, 초반 프로토타이핑 과정에서 주로 사용된 feature-daehan(강대한)과 feature-minh branch(황민)들은 clone된 후 main branch로 merge 없이 
개별 feature branch로 push되어서 github contributions에 나타나지 않습니다. Insights 메뉴 확인시 이 점 양해 부탁드립니다.


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

