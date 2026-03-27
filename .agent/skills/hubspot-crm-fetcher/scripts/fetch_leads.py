import requests
import argparse
import sys
from hs_auth_parser import get_hs_token

def fetch_leads(limit=10):
    try:
        token = get_hs_token()
    except Exception as e:
        print(f"Lỗi Xác Thực HubSpot (Auth Error): {e}")
        sys.exit(1)
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.hubapi.com/crm/v3/objects/contacts?limit={limit}&properties=email,firstname,lastname,phone,lifecyclestage,hs_lead_status'
    
    print(f"Fetching {limit} latest leads (contacts) from HubSpot CRM...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        contacts = data.get('results', [])
        
        # In header
        print(f"{'ID':<15} | {'Email':<30} | {'Name':<20} | {'Phone':<15} | {'Lifecycle/Status'}")
        print("-" * 105)
        
        for c in contacts:
            props = c.get('properties', {})
            id = c.get('id', '')
            email = (props.get('email') or '')[:30]
            name = (f"{props.get('firstname') or ''} {props.get('lastname') or ''}").strip()[:20]
            phone = (props.get('phone') or '')[:15]
            
            lifecycle = props.get('lifecyclestage') or ''
            lead_status = props.get('hs_lead_status') or ''
            status_display = f"{lifecycle}/{lead_status}".strip('/')
            
            print(f"{id:<15} | {email:<30} | {name:<20} | {phone:<15} | {status_display}")
    else:
        print(f"Error fetching leads. API returned {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch Leads from HubSpot")
    parser.add_argument('--limit', type=int, default=10, help='Number of leads to fetch')
    args = parser.parse_args()
    fetch_leads(args.limit)
