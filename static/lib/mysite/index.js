
Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

$(function(){
    // globals
    var    g_cellSide = 5;
    var    g_canvasHeight = window.innerHeight;

    var    g_canvasWidth = $("#canvascontainer").width();
    var    aImages = {}; // {id: imgid}
    var    g_imageCount = 200
    var    g_draw = 0;
    var    g_gap = 30;
    var    g_middle_bar_height = 30;

    function debug(str){
	objDebug = document.getElementById('debug')
	original = objDebug.innerHTML;
	original += "<BR>" + str;
	objDebug.innerHTML = original;
    }

    function initCanvasContainer(){
	$(".jumbotron_container").css("height", g_canvasHeight);
	$(".canvascontainer").css("height", g_canvasHeight);
	$(".middle-bar").css("top", g_canvasHeight - g_gap);
	$(".main_body_container").css("top", g_canvasHeight + g_gap + g_middle_bar_height);
	$(".sitename-rows").css("top", (g_canvasHeight - g_gap)/ 3);
    }

    function initCanvas(){
	canvas = document.getElementById("canvas"); // $("#canvas")[0]
	canvas.width = g_canvasWidth;
	canvas.height = g_canvasHeight;
	canvas.font = "bold 12px sans-serif";
	return canvas;
    }

    function getContext(convas){
	var ctx = canvas.getContext("2d");
	ctx.font = canvas.font;
	ctx.fillStyle = 'white';
	return ctx;
    }

    var canvas;
    var ctx;
    var images;

//    initCanvasContainer();
    
    if(g_draw > 0){
	canvas = initCanvas()
	ctx = getContext(canvas);
	drawCanvas(canvas, ctx);
    }

/*
    $.ajax({
	type: "GET",
	url: "/listpictures",
	data: { count: 200 }
    }).done(function( data ) {
	aImages = JSON.parse( data );
	images = createImages(aImages);
//	window.setInterval(function(){changeRow(canvas, ctx, images)}, 100);
    });
    */
    function getRandCSSColor(){
	var r, g, b;
	r = Math.floor(Math.random()*256);
	g = Math.floor(Math.random()*256);
	b = Math.floor(Math.random()*256);

	return "rgb(" + r + ", " + g + "," + b + ")";
    }

    function drawCanvas(canvas, ctx){
	for (x = 0; x < canvas.width; x += g_cellSide){
	    for (y = 0; y < canvas.height; y += g_cellSide){
		ctx.fillStyle = getRandCSSColor();
		ctx.fillRect(x, y, g_cellSide, g_cellSide);
	    }
	}
    }

    function createImages(aImages){
	var img;
	for (var id in aImages){
	    url = "/resource/image/fb/" + aImages[id] + ".jpg";
	    img = $('<img id="' + id + '">'); //Equivalent: $(document.createElement('img'))
	    img.attr('src', url);
	    img.attr('class', "fbimage");
	    
	    img.appendTo('#imgcontainer');
	}
	return img;
    }

    function changeRow(canvas, ctx, images){
	imageCount = g_imageCount;
	col = Math.floor(Math.random()*(canvas.width / g_cellSide + 1));
	line = Math.floor(Math.random()*(canvas.height / g_cellSide + 1));
	x = col * g_cellSide
	y = line * g_cellSide

	ctx.fillStyle = getRandCSSColor();
	ctx.fillRect(x, y, g_cellSide, g_cellSide);
	return;

	var img = $("img");
	ctx.drawImage(img.get(Math.floor(Math.random()*imageCount) - 2),x,y);
    }

    if(g_draw > 0){
	$(window).scroll(function () {
	    $('#debug').val($(window).scrollTop());
	    changeRow(canvas, ctx, images);
	});
    }

    $('#online-customer').css("width", window.innerWidth);

})
