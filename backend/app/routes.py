from flask import Blueprint, jsonify, request
import json
import winrm

api = Blueprint('api', __name__)

system_statuses = {}

def resolve_sid_to_name(sid):
    try:
        session = winrm.Session('http://localhost:5985/wsman', auth=('devashish', 'MummyJi@123'))  # Replace with actual credentials
        ps_script = f"[System.Security.Principal.SecurityIdentifier]::new('{sid}').Translate([System.Security.Principal.NTAccount]).Value"
        result = session.run_ps(ps_script)
        if result.status_code == 0:
            resolved_name = result.std_out.decode().strip()
            print(f"Resolved SID {sid} to {resolved_name}")
            return resolved_name
        else:
            print(f"Failed to resolve SID {sid}. Status code: {result.status_code}")
            print(f"Error message: {result.std_err.decode().strip()}")
    except Exception as e:
        print(f"Exception occurred while resolving SID {sid}: {str(e)}")
    return sid

def resolve_sids_in_statuses():
    for status in system_statuses.values():
        if 'policies' in status:
            for policy in status['policies']:
                original_sid = policy['user']
                policy['user'] = resolve_sid_to_name(policy['user'])
                print(f"Policy user SID {original_sid} resolved to {policy['user']}")

@api.route('/api/system_status', methods=['POST'])
def receive_status():
    data = request.get_json()
    system_statuses[data['hostname']] = data
    print("Received data:", json.dumps(data, indent=4))  # Pretty print received data
    print("Current system statuses:", json.dumps(system_statuses, indent=4))  # Pretty print stored statuses
    return jsonify({"message": "Status received"}), 200

@api.route('/api/system_status', methods=['GET'])
def get_status():
    resolve_sids_in_statuses()
    print("Returning system statuses:", json.dumps(system_statuses, indent=4))  # Pretty print statuses being returned
    return jsonify(system_statuses)
