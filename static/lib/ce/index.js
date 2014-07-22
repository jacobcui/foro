
$(document).ready(function(){
    windowWidth = window.innerWidth;
    
    $(window).scroll(function () {
	$('#debug').val($(window).scrollTop());
	$('#menu').css("top", $(window).scrollTop())
    });

    $('#online-customer').css("width", windowWidth);

    
});

$(function(){
    

})