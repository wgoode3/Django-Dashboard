$(document).ready(function(){

	// opens the login form modal
	$("#login").on('click', function(){
		$("#loginForm").modal();
		$("#myReg").hide();
		$("#myLog").show();
		$('#formType').text("Login");
	});
	
	// turns login form into a register form
	$("#switchType").on('click', function(){
		if($('#formType').text() == "Login"){
			$("#myReg").slideDown('slow');
			$("#myLog").hide();
			$('#formType').text("Register");
			$('#switchType').html(`<p id="switchType">Already a member? <a style="cursor:pointer;">Login</a></p>`)
		}else{
			$("#myReg").hide();
			$("#myLog").slideDown('slow');
			$('#formType').text("Login");
			$('#switchType').html(`<p id="switchType">Not a member? <a style="cursor:pointer;">Sign Up</a></p>`)
		}
	});

	// handles submitting the login data
	$('#submitLog').click(function(event){
		event.preventDefault();
		var data = $('#myLog form').serialize();
		$.post('/login', data, function(res){
			if(res.logged_in){
				window.location = '/home';
			}else{
				for(var i=0; i<res.errors.length; i++){
					error = `<div class="alert alert-danger alert-dismissable"><a href='' class="close" data-dismiss='alert' aria-label='close'>x</a>${res.errors[i]}</div>`;
					$('#validations').append(error);
				}
			}
		});
	});

	// handles submitting the registration data
	$('#submitReg').click(function(event){
		event.preventDefault();
		var data = $('#myReg form').serialize();
		$.post('/register', data, function(res){
			if(res.logged_in){
				window.location = '/home';
			}else{
				for(var i=0; i<res.errors.length; i++){
					error = `<div class="alert alert-danger alert-dismissable"><a href='' class="close" data-dismiss='alert' aria-label='close'>x</a>${res.errors[i]}</div>`;
					$('#validations').append(error);
				}
			}
		});
	});
	
});