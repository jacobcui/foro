function makeId(){var e="";var t="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(var n=0;n<5;n++)e+=t.charAt(Math.floor(Math.random()*t.length));return e}function sendingRequest(e,t,n,r){var i=new Array;var s=makeId();var o=e.length;var u=0;var a=1024;var f=0;var l=o;var c=0;while(l>0){if(c++>5){c=c}if(f+a>o){f=o}else{f=f+a}i.push(e.substring(u,f));l=o-f;u=f}for(var c=1;c<=i.length;c++){$.ajax({url:$host+"/report/generate/",dataType:"jsonp",data:{seq:c,total:i.length,action:"generate",appkey:n,token:s,data:i[c-1],format:t}})}}var $host="//www.foro.com.au"

