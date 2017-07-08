from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# regex requires at least 1 number, capital letter, lower case letter, permits some special characters !@#$%^&*+= and must be 8 characters or longer
PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')

class UserManager(models.Manager):
	def register(self, username, email, password, confirm_password):
		messages = []

		if len(username) < 1:
			messages.append('Username is required!')
		elif len(username) < 3:
			messages.append('Username must be 3 characters or more!')
		else:
			check = User.userManager.filter(username=username)
			if len(check) > 0:
				messages.append('Username already in use!')

		if len(email) < 1:
			messages.append('Email is required!')
		elif not EMAIL_REGEX.match(email):
			messages.append('Invalid Email!')
		else:
			check = User.userManager.filter(email=email.lower())
			if len(check) > 0:
				messages.append('Email already in use!')

		if len(password) < 1:
			messages.append('Password is required!')
		elif not PASSWORD_REGEX.match(password):
			messages.append('Password must contain at least 1 number and capitalization!')

		if len(confirm_password) < 1:
			messages.append('Confirm password is required!')
		elif confirm_password != password:
			messages.append('Password must match Confirm password!')

		if len(messages) < 1:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = User.userManager.create(username=username, email=email.lower(), password=pw_hash)
			return True, user
		else:
			return False, messages

	def login(self, email, password):
		messages = []

		if len(email) < 1:
			messages.append('Email is required!')
		elif not EMAIL_REGEX.match(email):
			messages.append('Invalid Email!')

		if len(password) < 1:
			messages.append('Password is required!')
		elif not PASSWORD_REGEX.match(password):
			messages.append('Password must contain at least 1 number and capitalization!')

		if len(messages) < 1:
			user = User.userManager.filter(email=email.lower())
			if len(user) < 1:
				return False, ['Email not found!']
			
			if bcrypt.checkpw(password.encode(), user[0].password.encode()):
				return True, user[0]
			else:
				return False, ['Incorrect Password!']
		else:
			return False, messages

	def change_pass(self, user_id, old_pass, new_pass, confirm_new_pass):
		
		user = User.userManager.get(id=user_id)
		messages = []

		if len(old_pass) < 1:
			messages.append('Old password is required!')
		elif not PASSWORD_REGEX.match(old_pass):
			messages.append('Old Password contains at least 1 number and capitalization!')

		if len(new_pass) < 1:
			messages.append('New password is required!')
		elif not PASSWORD_REGEX.match(new_pass):
			messages.append('New Password must contain at least 1 number and capitalization!')

		if len(confirm_new_pass) < 1:
			messages.append('Confirm new password is required!')
		elif confirm_new_pass != new_pass:
			messages.append('New password must match Confirm new password!')
			
		if len(messages) < 1:
			if not bcrypt.checkpw(old_pass.encode(), user.password.encode()):
				return False, ['Old password is incorrect!']
			else:
				user.password = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
				user.save()
				return True,
		else:
			return False, messages

	def user_update(self, user_id, username, email, description):

		messages = []

		if len(username) < 1:
			messages.append('Username is required!')
		elif len(username) < 3:
			messages.append('Username must be 3 characters or more!')
		else:
			check = User.userManager.filter(username=username)
			if len(check) > 0:
				if username != check[0].username:
					messages.append('Username already in use!')

		if len(email) < 1:
			messages.append('Email is required!')
		elif not EMAIL_REGEX.match(email):
			messages.append('Invalid Email!')
		else:
			check = User.userManager.filter(email=email.lower())
			if len(check) > 0:
				if email.lower() != check[0].email:
					messages.append('Email already in use!')
		
		if len(messages) > 0:
			return False, messages
		else:
			user = User.userManager.filter(id=user_id).update(username=username, email=email.lower(), description=description)
			return True, user

class User(models.Model):
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	is_admin = models.BooleanField(default=False)
	description = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()
	
	def __repr__(self):
		return "<User object: {} {}>".format(self.username, self.email)