$(document).ready(function(){
	
	$('#post_button').on('click', function(){
		$('#post_form').show();
		$('#post_button').hide();
	});

	$('.comment').on('click', function(){
		$(`#${$(this).attr('data-comment')}`).show();
		$(this).hide();
	});

});