from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def register(request):

	check = User.userManager.register(request.POST['username'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])

	if check[0]:
		request.session['user_id'] = check[1].id
		request.session['username'] = check[1].username
		request.session['admin'] = False
		response = {
			'logged_in': True,
			'user_id': check[1].id,
			'username': check[1].username
		}
		return JsonResponse(response)
	else:
		return JsonResponse({'logged_in': False, 'errors': check[1]})

def login(request):
	
	check = User.userManager.login(request.POST['email'], request.POST['password'])

	if check[0]:
		request.session['user_id'] = check[1].id
		request.session['username'] = check[1].username
		if check[1].is_admin:
			request.session['admin'] = True
		else:
			request.session['admin'] = False
		response = {
			'logged_in': True,
			'user_id': check[1].id,
			'username': check[1].username
		}
		return JsonResponse(response)
	else:
		return JsonResponse({'logged_in': False, 'errors': check[1]})

def logout(request):
	request.session.clear()
	messages.add_message(request, messages.SUCCESS, 'Log out successful!')
	return redirect(reverse('dashboard_index'))

def update(request, user_id):
	
	check = User.userManager.user_update(user_id, request.POST['username'], request.POST['email'], request.POST['description'])

	if check[0]:
		user = User.userManager.get(id=user_id)
		request.session['username'] = user.username
		messages.add_message(request, messages.SUCCESS, 'Update successful!')
		return redirect(reverse('dashboard_home'))
	else:
		for message in check[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/user/{}/edit'.format(user_id))

def change_pass(request, user_id):
	
	check = User.userManager.change_pass(user_id, request.POST['old_password'], request.POST['new_password'], request.POST['confirm_new_password'])

	if check[0]:
		messages.add_message(request, messages.SUCCESS, 'Password changed!')
		return redirect(reverse('dashboard_home'))
	else:
		for message in check[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/user/{}/edit'.format(user_id))

def change_level(request, user_id):
	if request.session['admin']:
		if request.POST['user_level'] == 'Admin':
			user = User.userManager.get(id=user_id)
			user.is_admin = True
			user.save()
			messages.add_message(request, messages.SUCCESS, 'You made {} an admin!'.format(user.username))
	# no method to remove an admin at the moment
	return redirect(reverse('dashboard_home'))

def delete(request, user_id):
	if request.session['admin']:
		user = User.userManager.get(id=user_id)
		user.delete() 
		messages.add_message(request, messages.SUCCESS, 'You deleted {}!'.format(user.username))
		return redirect(reverse('dashboard_home'))
	elif request.session['user_id'] == int(user_id):
		user = User.userManager.get(id=user_id).delete()
		request.session.clear()
		messages.add_message(request, messages.SUCCESS, 'You deleted your account!')
		return redirect(reverse('dashboard_index'))
	else:
		messages.add_message(request, messages.ERROR, 'You cannot delete that user!')
		return redirect(reverse('dashboard_home'))