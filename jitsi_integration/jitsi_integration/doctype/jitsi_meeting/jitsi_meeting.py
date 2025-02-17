# Copyright (c) 2025, Khizer Saeed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from jitsi_integration.www.meet.index import get_jitsi_meeting_url
from jitsi_integration.utils.jitsi_utils import generate_jitsi_meeting_token


class JitSiMeeting(Document):
	@frappe.whitelist()
	def go_to_meeting(self):
		response = get_jitsi_meeting_url(self.name)
		return response

	@frappe.whitelist()
	def send_invitation(self, domain):
		user_url = f"{domain}/?room={self.name}"
		self.invite_users(user_url)

	def invite_users(self, url):
		for participant in self.participants:
			self.send_invitation_email(participant.user, url)

	def invite_guests(self):
		for guest in self.guests:
			token = generate_jitsi_meeting_token(full_name=guest.full_name, email=guest.email)	
			url = f"{frappe.get_single('JitSi Settings').domain}/{self.meeting_name}?jwt={token}"
			self.send_invitation_email(guest.email, url)

	def send_invitation_email(self, email, url):
		message = f"You are invited to join the meeting. Please click on the link below to join the meeting. <br> {url} <br> <strong>Meeting Details:</strong> {self.meeting_details}"
		frappe.sendmail(
			recipients=[email],
			subject=self.meeting_agenda,
			message=message
		)