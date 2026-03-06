#!/usr/bin/env python3
"""
환율 그래프 생성 스크립트
matplotlib을 사용하여 환율 변동 그래프 생성
"""

import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 파일 경로
DATA_FILE = Path(__file__).parent.parent / "references" / "exchange-rates.json"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

def load_data():
    """환율 데이터 로드"""
    if not DATA_FILE.exists():
        print("No data file found")
        return None
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("rates", [])

def plot_daily_graph(rates, days=7):
    """일별 환율 그래프 생성"""
    if not rates:
        print("No rates to plot")
        return None
    
    # 최근 N일 데이터 필터링
    recent_rates = rates[-(days*4):]  # 하루 4번 * N일
    
    # 데이터 준비
    timestamps = [datetime.fromtimestamp(r['timestamp']) for r in recent_rates]
    values = [r['rate'] for r in recent_rates]
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(timestamps, values, marker='o', markersize=3, linewidth=1.5, color='#1f77b4')
    ax.fill_between(timestamps, values, alpha=0.3)
    
    # 포맷팅
    ax.set_title(f'USD/KRW Exchange Rate (Last {days} Days)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date/Time', fontsize=11)
    ax.set_ylabel('Exchange Rate (KRW)', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # x축 포맷
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    plt.xticks(rotation=45, ha='right')
    
    # y축 포맷
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    plt.tight_layout()
    
    # 저장
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f'exchange_rate_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Graph saved: {output_file}")
    return output_file

def plot_trend_graph(rates):
    """추세 그래프 (일별 평균)"""
    if not rates:
        return None
    
    # 날짜별로 그룹화
    daily_rates = {}
    for r in rates:
        date = r['date']
        if date not in daily_rates:
            daily_rates[date] = []
        daily_rates[date].append(r['rate'])
    
    # 평균 계산
    dates = sorted(daily_rates.keys())
    avg_rates = [sum(daily_rates[d]) / len(daily_rates[d]) for d in dates]
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
    ax.plot(x_dates, avg_rates, marker='o', markersize=6, linewidth=2, color='#2ca02c')
    ax.fill_between(x_dates, avg_rates, alpha=0.3, color='#2ca02c')
    
    # 포맷팅
    ax.set_title('USD/KRW Daily Average Rate', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('Average Rate (KRW)', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    plt.tight_layout()
    
    # 저장
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f'exchange_rate_trend_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Trend graph saved: {output_file}")
    return output_file

def generate_mermaid_chart(rates, days=7):
    """Mermaid XY Chart 생성"""
    if not rates:
        return None
    
    # 최근 데이터 필터링
    recent_rates = rates[-(days*4):]
    
    # Mermaid xychart-beta 형식으로 변환
    x_labels = [f"{r['date'][5:]}" for r in recent_rates]  # MM-DD
    y_values = [r['rate'] for r in recent_rates]
    
    # 최소/최대값 계산
    min_val = int(min(y_values) - 10)
    max_val = int(max(y_values) + 10)
    
    mermaid = f"""```mermaid
xychart-beta
    title "USD/KRW Exchange Rate"
    x-axis [{', '.join(x_labels[:10])}]
    y-axis "KRW" {min_val} --> {max_val}
    line [{', '.join([str(v) for v in y_values[:10]])}]
```"""
    
    return mermaid

def main():
    """메인 실행"""
    rates = load_data()
    
    if not rates:
        print("No data available")
        return
    
    print(f"📊 Total rates collected: {len(rates)}")
    
    # 일별 그래프
    daily_graph = plot_daily_graph(rates, days=7)
    
    # 추세 그래프
    trend_graph = plot_trend_graph(rates)
    
    # Mermaid 차트
    mermaid_chart = generate_mermaid_chart(rates, days=7)
    if mermaid_chart:
        print("\n📊 Mermaid Chart:")
        print(mermaid_chart)
    
    return {
        "daily_graph": str(daily_graph) if daily_graph else None,
        "trend_graph": str(trend_graph) if trend_graph else None,
        "mermaid_chart": mermaid_chart
    }

if __name__ == "__main__":
    main()
