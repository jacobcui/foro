
function parseResponse(data){
    jobj=data
    if (jobj.statuscode != 0){
	$("#filelinks").html(
	    "<div class='span9'> Creation failed: "+ jobj.statuscode +":" + jobj.errormessage + " </div>"
	);
    }else{
	$("#filelinks").html(
	    "<div class='span9'> File: <a href=" + $host + jobj.link + ">"+ jobj.filename +"</a></label> </div>"
	);
    }
    $("#create").html("Create ");
}

$(function(){
    var xlsdata = $("#xlsdata").val();
    var format = 'json';

    $("#create").click(function(){
	$("#create").html("Create <img style=\"height:19px\" src=\"/resource/image/loading.gif\">");
	sendingRequest($("#xlsdata").val(), format, 'APPDEMO_EXCEL', parseResponse)
    })

    $("#textselect").click(function(){
	$("#xlsdata").html($("#textdata").html());
	format = 'text';
    })

    $("#jsonselect").click(function(){
	$("#xlsdata").html($("#jsondata").html());
	format = 'json';
    })
})
