$(function(){
    $(".btnselect").click(function(){
	$planid = $(this).attr('id');
	$.ajax({
	    type: 'GET',
	    url: '/report/getplan/' + $planid,
	}).done(function(data){
	    $("#plan_details_container").addClass("shadow");
	    $("#plan_details").html(data);
	});
    });

})
