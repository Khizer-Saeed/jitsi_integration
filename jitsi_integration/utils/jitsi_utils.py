import jwt
import frappe

@frappe.whitelist()
def generate_jitsi_meeting_token():
    jitsi_settings = frappe.get_single("JitSi Settings")
    # configureable in JitSi Integration Settings
    App_Secret = jitsi_settings.get_password("secret_token")
    Issuers=jitsi_settings.issuers
    Audiences=jitsi_settings.audiences
    Domain=jitsi_settings.domain

    if frappe.session.user and frappe.db.exists("User", frappe.session.user):
        user = frappe.get_doc("User", frappe.session.user)

        if user.full_name and user.email:
            payload =  {
                "context": {
                    "user": {
                        "name": user.full_name,
                        "email": user.email
                    }
                },
                "aud": Issuers,
                "iss": Audiences,
                "sub": Domain,
                "room": "*"
            }
            
            encoded_jwt = jwt.encode(payload, App_Secret, algorithm="HS256")
            return encoded_jwt
    else:
        frappe.throw("User doesn't exist")
