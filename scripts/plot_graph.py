#!/usr/bin/env python3
"""
환율 그래프 생성 스크립트
USD/KRW, USD/VND 환율 그래프 생성 (리스트 + 스파크라인)
"""

import json
from datetime import datetime
from pathlib import Path

# 파일 경로
DATA_FILE = Path(__file__).parent.parent / "references" / "exchange-rates.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

def load_data():
    """환율 데이터 로드"""
    if not DATA_FILE.exists():
        print("No data file found")
        return None, None
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("krw_rates", []), data.get("vnd_rates", [])

def generate_sparkline(values, bars=8):
    """스파크라인 생성 (유니코드 블록)"""
    if not values or len(values) < 2:
        return "▁"
    
    # 최근 N개만 사용
    recent = values[-bars:]
    
    # 정규화
    min_val = min(recent)
    max_val = max(recent)
    range_val = max_val - min_val
    
    # 스파크라인 문자: ▁ ▂ ▃ ▄ ▅ ▆ ▇ █
    spark_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    
    sparkline = ""
    for val in recent:
        if range_val > 0:
            idx = int((val - min_val) / range_val * (len(spark_chars) - 1))
        else:
            idx = 3  # 중간값
        sparkline += spark_chars[idx]
    
    return sparkline

def get_trend(values):
    """추세 분석 (상승/하락/보합)"""
    if not values or len(values) < 2:
        return "→"
    
    recent = values[-4:]  # 최근 4개
    if len(recent) < 2:
        return "→"
    
    current = recent[-1]
    previous = recent[-2]
    
    diff = current - previous
    
    if diff > 0:
        return f"↑ +{diff:,.1f}"
    elif diff < 0:
        return f"↓ {diff:,.1f}"
    else:
        return "→"

def generate_report(krw_rates, vnd_rates):
    """환율 리포트 생성 (리스트 형태)"""
    if not krw_rates:
        return "❌ 데이터 없음"
    
    output = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    output.append(f"💱 **환율 리포트** ({now})")
    output.append("━" * 40)
    
    # 현재 환율
    output.append("\n**현재 환율**")
    
    if krw_rates:
        latest = krw_rates[-1]
        current_krw = latest['rate']
        date_str = f"{latest['date']} {latest['time']}"
        sparkline_krw = generate_sparkline([r['rate'] for r in krw_rates])
        trend_krw = get_trend([r['rate'] for r in krw_rates])
        output.append(f"- 🇰🇷 **USD/KRW** ({date_str}): {current_krw:,.1f}원 {sparkline_krw} {trend_krw}")
    
    if vnd_rates:
        latest = vnd_rates[-1]
        current_vnd = latest['rate']
        date_str = f"{latest['date']} {latest['time']}"
        sparkline_vnd = generate_sparkline([r['rate'] for r in vnd_rates])
        trend_vnd = get_trend([r['rate'] for r in vnd_rates])
        output.append(f"- 🇻🇳 **USD/VND** ({date_str}): {current_vnd:,.0f}동 {sparkline_vnd} {trend_vnd}")
    
    # 7일 추세
    output.append("\n**7일 추세**")
    
    if krw_rates and len(krw_rates) >= 7:
        week_krw = [r['rate'] for r in krw_rates[-7:]]
        min_krw = min(week_krw)
        max_krw = max(week_krw)
        avg_krw = sum(week_krw) / len(week_krw)
        output.append(f"- KRW: {min_krw:,.0f} ~ {max_krw:,.0f} (평균 {avg_krw:,.0f})")
    
    if vnd_rates and len(vnd_rates) >= 7:
        week_vnd = [r['rate'] for r in vnd_rates[-7:]]
        min_vnd = min(week_vnd)
        max_vnd = max(week_vnd)
        avg_vnd = sum(week_vnd) / len(week_vnd)
        output.append(f"- VND: {min_vnd:,.0f} ~ {max_vnd:,.0f} (평균 {avg_vnd:,.0f})")
    
    output.append("━" * 40)
    
    return "\n".join(output)

def main():
    """메인 실행"""
    krw_rates, vnd_rates = load_data()
    
    if not krw_rates and not vnd_rates:
        print("❌ 데이터 없음")
        return
    
    # 리포트 생성
    report = generate_report(krw_rates, vnd_rates)
    print("\n" + report)
    
    # 출력 디렉토리 생성
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 파일로 저장
    report_file = OUTPUT_DIR / f"exchange_rate_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 저장됨: {report_file}")
    
    return {
        "report_file": str(report_file),
        "krw_count": len(krw_rates),
        "vnd_count": len(vnd_rates) if vnd_rates else 0
    }

if __name__ == "__main__":
    main()
