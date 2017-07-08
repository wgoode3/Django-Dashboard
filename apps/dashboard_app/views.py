from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Post, Comment

def index(request):
	return render(request, 'dashboard_app/index.html')

def home(request):
	if 'user_id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must log in or register!')
		return redirect(reverse('dashboard_index'))

	# make a user admin
	# user = User.userManager.get(id=request.session['user_id'])
	# user.is_admin = True
	# user.save()

	users = User.userManager.all()

	return render(request, 'dashboard_app/home.html', {'users': users})

def edit(request, user_id):
	if 'user_id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must log in or register!')
		return redirect(reverse('dashboard_index'))

	if not request.session['admin']:
		if request.session['user_id'] != int(user_id):
			# maybe include an error message as well
			return redirect(reverse('dashboard_home'))
	user = User.userManager.get(id=user_id)
	return render(request, 'dashboard_app/edit.html', {'user': user})

def board(request, user_id):
	if 'user_id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must log in or register!')
		return redirect(reverse('dashboard_index'))
		
	context = {
		'user': User.userManager.get(id=user_id),
		'posts': Post.postManager.filter(user_board_id=user_id),
	}
	return render(request, 'dashboard_app/board.html', context)

def post(request, board_id):
	post = Post.postManager.post(board_id, request.session['user_id'], request.POST['post'])
	return redirect('/user/{}/board'.format(board_id))

def comment(request, post_id):
	board_id = request.POST['board']
	comment = Comment.commentManager.comment(post_id, request.session['user_id'], request.POST['comment'])
	return redirect('/user/{}/board'.format(board_id))