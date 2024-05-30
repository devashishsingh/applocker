import time
import requests
import logging
import os

# Setup logging
logging.basicConfig(filename='agent.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s')

def get_applocker_status():
    # Implement your logic to fetch AppLocker status and policies
    status = {
        'hostname': os.getenv('COMPUTERNAME', 'Unknown'),
        'ip': requests.get('https://api.ipify.org').text,
        'applocker_status': 'Enabled',
        'applocker_policy_xml': '<AppLockerPolicy><RuleCollection Type="Exe"><FilePathRule Id="1" Name="Example Rule" UserOrGroupSid="S-1-1-0" Action="Allow"><Conditions><FilePathCondition Path="C:\\Program Files\\*" /></Conditions></FilePathRule></RuleCollection></AppLockerPolicy>'
    }
    return status

def send_status():
    url = 'http://localhost:5000/api/system_status'
    headers = {'Content-Type': 'application/json'}
    while True:
        try:
            status = get_applocker_status()
            response = requests.post(url, json=status, headers=headers)
            if response.status_code == 200:
                logging.info("Status sent successfully")
            else:
                logging.error(f"Failed to send status: {response.status_code}")
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
        time.sleep(60)  # Send status every 60 seconds

if __name__ == '__main__':
    logging.info("Agent service starting")
    send_status()
