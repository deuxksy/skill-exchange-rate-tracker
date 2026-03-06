#!/usr/bin/env python3
"""
하나은행 환율 수집 스크립트
USD/KRW 환율을 조회해서 JSON 파일로 저장
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import time

# 데이터 파일 경로
DATA_FILE = Path(__file__).parent.parent / "references" / "exchange-rates.json"

def fetch_hana_bank_rate():
    """하나은행 환율 조회 (웹 스크래핑 또는 API)"""
    try:
        # 하나은행 환율 페이지
        url = "https://www.kebhana.com/cont/mall/mall01/mall0101/index.jsp"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        # 실제 구현시에는 HTML 파싱 필요
        # 여기서는 예시로 None 반환
        return None
    except Exception as e:
        print(f"Error fetching from Hana Bank: {e}")
        return None

def fetch_fallback_rate():
    """백업: 무료 환율 API 사용"""
    try:
        # ExchangeRate-API (무료)
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        krw_rate = data['rates'].get('KRW')
        return krw_rate
    except Exception as e:
        print(f"Error fetching fallback rate: {e}")
        return None

def load_data():
    """기존 데이터 로드"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"rates": []}

def save_rate(rate):
    """환율 데이터 저장"""
    data = load_data()
    now = datetime.now()
    
    new_entry = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "rate": round(rate, 2),
        "timestamp": int(now.timestamp())
    }
    
    data["rates"].append(new_entry)
    
    # 저장
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved: {new_entry}")
    return new_entry

def main():
    """메인 실행"""
    print(f"Fetching exchange rate at {datetime.now()}")
    
    # 하나은행 시도
    rate = fetch_hana_bank_rate()
    
    # 실패시 백업 API 사용
    if rate is None:
        print("Trying fallback API...")
        rate = fetch_fallback_rate()
    
    if rate:
        entry = save_rate(rate)
        print(f"✅ USD/KRW: {rate:,.2f}원")
        return entry
    else:
        print("❌ Failed to fetch exchange rate")
        return None

if __name__ == "__main__":
    main()
