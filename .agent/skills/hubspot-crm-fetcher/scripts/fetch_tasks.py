import requests
import argparse
import sys
from hs_auth_parser import get_hs_token

def fetch_tasks(limit=10):
    try:
        token = get_hs_token()
    except Exception as e:
        print(f"Lỗi Xác Thực HubSpot (Auth Error): {e}")
        sys.exit(1)
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.hubapi.com/crm/v3/objects/tasks?limit={limit}&properties=hs_task_subject,hs_task_status,hs_task_priority'
    
    print(f"Fetching {limit} latest tasks from HubSpot CRM...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        tasks = data.get('results', [])
        
        # In header
        print(f"{'ID':<15} | {'Subject':<40} | {'Status':<15} | {'Priority':<10}")
        print("-" * 90)
        
        for t in tasks:
            props = t.get('properties', {})
            id = t.get('id', '')
            subject = (props.get('hs_task_subject') or '')[:40]
            status = (props.get('hs_task_status') or '')[:15]
            priority = (props.get('hs_task_priority') or '')[:10]
            
            print(f"{id:<15} | {subject:<40} | {status:<15} | {priority:<10}")
    else:
        print(f"Error fetching tasks. API returned {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch Tasks from HubSpot")
    parser.add_argument('--limit', type=int, default=10, help='Number of tasks to fetch')
    args = parser.parse_args()
    fetch_tasks(args.limit)
