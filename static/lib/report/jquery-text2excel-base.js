
var $host="//www.foro.com.au";
//$host="http://127.0.0.1";

function makeId(){
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function sendingRequest(text, type, appkey, callback){
    var strary = new Array();
    var $token = makeId();
    var len = text.length;
    var f = 0; var gap = 512; var t = 0;
    var remain = len
    var i = 0;

    while(remain > 0){
	if( (t + gap) > len ){
            t = len 
	}else{
            t = t + gap;
	}

        strary.push(text.substring(f, t));
	remain = len - t
        f = t;
    }

    for( var i = 1; i <= strary.length; i++){
       $.ajax({
            url: $host + "/report/generate/",
            dataType: "jsonp",
            data: {
                seq: i,
                total: strary.length,
                action: 'generate',
                appkey: appkey,
                token: $token,
                data: strary[i - 1],
                format: type
            }
        });
    }
}
