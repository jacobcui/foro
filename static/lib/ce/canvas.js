$(function(){
    positions = new Array();
    singlePos = {'x': 0, 'y': 0};

    function getRadian(degrees){
	return degrees * Math.PI / 180.0;
    }

    function getNextPos(singlePos, degree){
	x = parseInt(singlePos.x) - 20;
	y = parseInt(singlePos.y) + 20;
	return {'x': x, 'y': y};
    }

    function debug(str){
	objDebug = document.getElementById('debug')
	original = objDebug.innerHTML;
	original += "<BR>" + str;
	objDebug.innerHTML = original;
	
    }

    basex = 100
    basey = 100
    g_canvasHeight = 200;
    g_canvasWidth = window.innerWidth;

    contents = new Array(
	{text: "Customer ", x: basex, y: basey, angel: 0, font:"40px Arial", angel: 0},
	{text: "Explorer ", x: basex , y: basey + 40, angel: 0, font:"36px Arial", angel: 0},
	{text: "John ", x: basex - 10, y: basey -15, angel: 270},
	{text: "backed by a ", x: basex - 30, y: basey - 40, angel: 270},
	{text: "team of in-house experts. ", x: basex, y: basey, angel: 0},
	{text: "At last", x: basex, y: basey, angel: 0},
	{text: "a system ", x: basex, y: basey, angel: 0},
	{text: "that is truly intuitive and simple to use. ", x: basex, y: basey, angel: 0},
	{text: "If you know how to browse the internet", x: basex, y: basey, angel: 0},
	{text: "you'll be able to use ", x: basex, y: basey, angel: 0},
	{text: "LoanKit's software with minimal training", x: basex, y: basey, angel: 0}
    )
    cnv = document.getElementById("cnv");
    cnv.width = g_canvasWidth;
    cnv.height = g_canvasHeight;

    cnv.font = "bold 12px sans-serif";
    ctx = cnv.getContext("2d");
    ctx.font = cnv.font;

    initialDegree = 0;

    // Globals
    $g_hwRatio = 2; // font height to width ratio
    $g_canvasArea = {left: 0, top:0, right: 600, bottom: 400};
    $g_occupiedArea = new Array(); // contains area structs {left: x, top:x, right:x, bottom:x}
    $g_maxHeight = 40; // font's max height
    $g_minHeight = 10; // font's min height

    function getRandCSSColor(){
	var r, g, b;
	r = Math.floor(Math.random()*256);
	g = Math.floor(Math.random()*256);
	b = Math.floor(Math.random()*256);

	res = "rgb(" + r + ", " + g + "," + b + ")";
	return res;

    }

    g_cellSide = 50;

    ctx.fillStyle = 'white';
    for (x = 0; x < cnv.width; x += g_cellSide){
	for (y = 0; y < cnv.height; y += g_cellSide){
	    ctx.fillStyle = getRandCSSColor();
	    ctx.fillRect(x, y, g_cellSide, g_cellSide);
	}
    }

    function createFbPictures(id, src){
	return $('<img>', { id: id, src: src});
    }


    var imgcontainer = $("#imgcontainer");	
    var g_imgcount = 500
    for (i =0; i< g_imgcount; i++){
	id = 100001437118470 + i;
	url = "/resource/image/fb/" + id + ".jpg";
	var img = $('<img id="' + id + '">'); //Equivalent: $(document.createElement('img'))
	img.attr('src', url);
	img.attr('class', "fbimage");
	
	img.appendTo('#imgcontainer');
    }

    function changeLine(){
	col = Math.floor(Math.random()*(cnv.width / g_cellSide + 1));
	line = Math.floor(Math.random()*(cnv.height / g_cellSide + 1));
	//    ctx.fillStyle = getRandCSSColor();
	x = col * g_cellSide
	y = line * g_cellSide
	//    ctx.fillStyle = "#FFFFFF"
	//    ctx.fillRect(x, y, g_cellSide, g_cellSide)
	    var img = $("img");
	ctx.drawImage(img.get(Math.floor(Math.random()*g_imgcount)),x,y);
    }

    window.setInterval(changeLine, 100);

    if(0){
	for (i = 0; i< contents.length; i++){
	    if ( i == 7){break;}
	    content = contents[i];
	    ctx.setTransform(1,0,0,1,0,0);

	    ctx.translate(content.x, content.y);

	    ctx.rotate(getRadian(content.angel));

	    if(typeof content.font != 'undefined'){
		ctx.font = content.font;
	    }else{
		ctx.font = cnv.font;
	    }
	    ctx.textBaseline="top"; 
	    //ctx.fillText(content.text + "(" + content.x + ", " + content.y + ")", 0, 0);
	    ctx.fillText(content.text, 0, 0);
	    ctx.beginPath();
	    ctx.moveTo(0,0);
	    ctx.lineTo(50,0);
	    ctx.stroke();

	    debug("Degree: " + content.angel + " (" +getRadian(content.angel) + ") x: " + content.x + " y: " + content.y  + " &nbsp; Text: " + content.text + " __" + (-content.x) + ", " + (-content.y));
	    ctx.rotate(0 - getRadian(content.angel));
	    ctx.translate( -content.x,  -content.y);
	}
    }

})
