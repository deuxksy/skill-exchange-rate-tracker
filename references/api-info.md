# 환율 API 정보

## 하나은행 (1차)

- **웹사이트:** https://www.kebhana.com/cont/mall/mall01/mall0101/index.jsp
- **방법:** 웹 스크래핑
- **주의:** robots.txt 확인 필요, 과도한 요청 금지

## 백업 API (2차)

### ExchangeRate-API (무료)
- **URL:** https://www.exchangerate-api.com/
- **제한:** 하루 1,500회
- **데이터:** USD/KRW 포함
- **API:** `https://api.exchangerate-api.com/v4/latest/USD`

### 한국은행 경제통계시스템 (공식)
- **URL:** https://ecos.bok.or.kr/
- **API 키 필요:** 무료 발급 가능
- **데이터:** 공식 환율 데이터

## 데이터 저장

- **파일:** `references/exchange-rates.json`
- **형식:**
```json
{
  "rates": [
    {
      "date": "2026-03-06",
      "time": "09:00",
      "rate": 1485.50,
      "timestamp": 1772806800
    }
  ]
}
```

## 출력 형식

- **Mermaid XY Chart** - Markdown에서 바로 렌더링
- **PNG 이미지** - `output/` 폴더에 저장

### 예시 그래프 (Mermaid)

```mermaid
xychart-beta
    title "USD/KRW Exchange Rate"
    x-axis [09:00, 12:00, 15:00, 18:00]
    y-axis "KRW" 1450 --> 1520
    line [1485, 1488, 1483, 1490]
```
