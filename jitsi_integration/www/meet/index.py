import frappe
from jitsi_integration.utils.jitsi_utils import generate_jitsi_meeting_token

def check_user_in_participants(room):
    if frappe.db.exists("JitSi Meeting", room):
        jitsi_meeting = frappe.get_doc("JitSi Meeting", room)
        is_participant = [False, "You are not in participants list"]
        for jitsi_participant in jitsi_meeting.participants:
            if jitsi_participant.user == frappe.session.user:
                is_participant = [True, jitsi_meeting.meeting_name]
                break
                
        return is_participant
    else:
        return [False, "Meeting not found"]
        
@frappe.whitelist()
def get_jitsi_meeting_url(room):
    if frappe.session.user and frappe.session.user != "Guest" and frappe.db.exists("User", frappe.session.user):
        meeting_info = check_user_in_participants(room)
        if meeting_info[0]:
            domain = frappe.get_single("JitSi Settings").domain
            jitsi_meeting_token = generate_jitsi_meeting_token()
            if jitsi_meeting_token:
                meeting_url = f"https://{domain}/{meeting_info[1]}?jwt={jitsi_meeting_token}"
                return [True, meeting_url]
            else:
                return [False, "Error while generating token"]
        else:
            return meeting_info
    else:
        return [False, "User doesn't exist"]