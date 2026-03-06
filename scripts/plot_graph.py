#!/usr/bin/env python3
"""
환율 그래프 생성 스크립트
USD/KRW, USD/VND 환율 그래프 생성
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

def generate_mermaid_chart(krw_rates, vnd_rates, days=7):
    """Mermaid XY Chart 생성"""
    if not krw_rates:
        return None
    
    # 최근 데이터 필터링
    recent_krw = krw_rates[-(days*4):] if len(krw_rates) > days*4 else krw_rates
    recent_vnd = vnd_rates[-(days*4):] if vnd_rates and len(vnd_rates) > days*4 else vnd_rates
    
    # 데이터 준비
    x_labels = [f"{r['date'][5:]} {r['time']}" for r in recent_krw]
    krw_values = [r['rate'] for r in recent_krw]
    vnd_values = [r['rate'] for r in recent_vnd] if recent_vnd else []
    
    # Mermaid xychart-beta 형식 (GitHub 미지원으로 ASCII 아트 사용)
    output = []
    output.append("📊 USD/KRW & USD/VND Exchange Rate")
    output.append("━" * 50)
    
    # KRW 그래프
    if krw_values:
        max_val = max(krw_values)
        min_val = min(krw_values)
        range_val = max_val - min_val
        
        output.append("\n🇰🇷 USD/KRW (원화):")
        for i, (label, val) in enumerate(zip(x_labels, krw_values)):
            bar_len = int((val - min_val) / range_val * 20) if range_val > 0 else 10
            bar = "█" * bar_len
            output.append(f"{label}: {bar} {val:,.0f}")
    
    # VND 그래프
    if vnd_values:
        max_val = max(vnd_values)
        min_val = min(vnd_values)
        range_val = max_val - min_val
        
        output.append("\n🇻🇳 USD/VND (베트남 동화):")
        for i, (label, val) in enumerate(zip(x_labels, vnd_values)):
            bar_len = int((val - min_val) / range_val * 20) if range_val > 0 else 10
            bar = "█" * bar_len
            output.append(f"{label}: {bar} {val:,.0f}")
    
    return "\n".join(output)

def generate_ascii_graph(krw_rates, vnd_rates, days=7):
    """ASCII 아트 그래프 생성 (GitHub 호환)"""
    if not krw_rates:
        return "No data available"
    
    # 최근 데이터 필터링
    recent_krw = krw_rates[-(days*4):] if len(krw_rates) > days*4 else krw_rates
    recent_vnd = vnd_rates[-(days*4):] if vnd_rates and len(vnd_rates) > days*4 else vnd_rates
    
    output = []
    output.append("```")
    output.append("📊 Exchange Rates (Last {} Days)".format(days))
    output.append("━" * 50)
    
    # KRW
    if recent_krw:
        output.append("\n🇰🇷 USD/KRW:")
        for r in recent_krw[-10:]:  # 최근 10개만 표시
            output.append(f"  {r['date']} {r['time']} → {r['rate']:,.0f}원")
    
    # VND
    if recent_vnd:
        output.append("\n🇻🇳 USD/VND:")
        for r in recent_vnd[-10:]:  # 최근 10개만 표시
            output.append(f"  {r['date']} {r['time']} → {r['rate']:,.0f}동")
    
    output.append("```")
    
    return "\n".join(output)

def main():
    """메인 실행"""
    krw_rates, vnd_rates = load_data()
    
    if not krw_rates and not vnd_rates:
        print("No data available")
        return
    
    print(f"📊 Total rates collected:")
    print(f"   KRW: {len(krw_rates)} entries")
    print(f"   VND: {len(vnd_rates) if vnd_rates else 0} entries")
    
    # ASCII 그래프 생성
    ascii_graph = generate_ascii_graph(krw_rates, vnd_rates, days=7)
    print("\n" + ascii_graph)
    
    # 출력 디렉토리 생성
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 그래프 파일로 저장
    graph_file = OUTPUT_DIR / f"exchange_rate_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(graph_file, 'w', encoding='utf-8') as f:
        f.write(ascii_graph)
    
    print(f"\n✅ Graph saved: {graph_file}")
    
    return {
        "graph_file": str(graph_file),
        "krw_count": len(krw_rates),
        "vnd_count": len(vnd_rates) if vnd_rates else 0
    }

if __name__ == "__main__":
    main()
