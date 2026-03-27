import os
import yaml

def get_hs_token():
    config_path = os.path.expanduser('~/.hscli/config.yml')
    if not os.path.exists(config_path):
        raise Exception("Không tìm thấy ~/.hscli/config.yml. Vui lòng chạy hs auth trước.")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Support both old 'portals' and new 'accounts' structures
    portals = config.get('accounts', config.get('portals', []))
    default_portal_id = config.get('defaultAccount', config.get('defaultPortal'))
    
    portal_config = None
    if default_portal_id:
        for portal in portals:
            curr_id = portal.get('accountId', portal.get('portalId'))
            if str(curr_id) == str(default_portal_id):
                portal_config = portal
                break
                
    if not portal_config and len(portals) > 0:
        portal_config = portals[0]
        
    if not portal_config:
        raise Exception("Không tìm thấy cấu hình portal/account trong ~/.hscli/config.yml")
        
    # Get the token (try PAT first, then OAuth, then token root)
    token = portal_config.get('personalAccessKey')
    if not token:
        token = portal_config.get('auth', {}).get('tokenInfo', {}).get('accessToken')
    if not token:
        token = portal_config.get('oauth2', {}).get('accessToken')
    if not token:
        token = portal_config.get('token')
        
    if not token:
        raise Exception("Không trích xuất được token hợp lệ. Vui lòng check lại file ~/.hscli/config.yml")
    
    # Replace newlines if it's a folded string from YAML
    return token.replace('\n', '').replace('\r', '').strip()
