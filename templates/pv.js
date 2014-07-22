
var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;
var ZOOM_DELTA = 120;

var camera, scene, renderer, focus;
var canvasid = 'pv_canvas_{{ pv_username }}_{{ pv_textid }}';
var floorid = 'pv_floor_{{ pv_username }}_{{ pv_textid }}';
var floor_imageid = 'pv_floor_image';

var pan_lt = 'pan_lt';
var pan_rt = 'pan_rt';
var pan_up = 'pan_up';
var pan_down = 'pan_down';
var pan_timer;

var zoom_in = 'zoom_in';
var zoom_out = 'zoom_out';

var lon = 0, lat = 0;
var phi = 0, theta = 0;
var pointLight, light;

var canvasWidth = {{pv_scene_width}};
var canvasHeight = {{pv_scene_height}};
// console.log(canvasHeight);
// console.log(getParentHeight(canvasid));
// console.log(getDom(domId).parentNode.getAttribute('id'))


function getjid(domId){
    return '#' + domId;
}

function getDom(domId){
    return document.getElementById(domId);
}

function getDomParent(domId){
    return getDom(domId).parentNode;
}

function getParentHeight(domId){
    return getDomParent(domId).offsetHeight;
}

function getParentWidth(domId){
    return getDomParent(domId).offsetWidth;
}

function getCanvasWidth(canvasId){
    return getParentWidth(canvasId);
}

function getCanvasHeight(canvasId){
    return getParentHeight(canvasId);
}

init();
render();

if(0){
$( getjid(floorid) ).hide();
$( getjid(floorid) ).height(getParentHeight(floorid));

$( getjid(floor_imageid) ).attr("src", "/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/fp");
$("#floorplan-nav-btn").click(function(){
    $( getjid(floorid) ).toggle( "slide" );

    if($(this).html() == "&gt;&gt;"){
	$(this).html("<<");
    }else{
	$(this).html(">>");
    }
});
}


function init(){
    // set the scene size
    getDomParent(canvasid).style.height = canvasHeight + "px";

    var side_len = getCanvasWidth(canvasid);
    var center_distance = side_len / 2.0;

// set some camera attributes
    VIEW_ANGLE = 60;  NEAR = 0.1;    FAR = 10000;

    camera = new THREE.PerspectiveCamera(VIEW_ANGLE, getCanvasWidth(canvasid) / getCanvasHeight(canvasid), NEAR, FAR);
    scene = new THREE.Scene();
    scene.add(camera);     // add the camera to the scene

    renderer = new THREE.CSS3DRenderer();
    renderer.setSize(getCanvasWidth(canvasid), getCanvasHeight(canvasid));
    
    focus = new THREE.Vector3( 0, 0, -center_distance );
    
    var name = '{{ pv_scene_name }}';
// /get/scene/panoview/index/f
    
    var sides = [
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/r',
	    position: [ -center_distance, 0, 0 ],
	    rotation: [ 0, Math.PI / 2, 0 ]
	},
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/l',
	    position: [ center_distance, 0, 0 ],
	    rotation: [ 0, -Math.PI / 2, 0 ]
	},
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/u',
	    position: [ 0,  center_distance, 0 ],
	    rotation: [ Math.PI / 2, 0, Math.PI ]
	},
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/d',
	    position: [ 0, -center_distance, 0 ],
	    rotation: [ - Math.PI / 2, 0, Math.PI ]
	},
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/f',
	    position: [ 0, 0,  center_distance ],
	    rotation: [ 0, Math.PI, 0 ]
	},
	{
	    url: '/get/scene/{{ pv_username}}/{{pv_textid}}/{{pv_index}}/b',
	    position: [ 0, 0, -center_distance ],
	    rotation: [ 0, 0, 0 ]
	}
    ];

    for ( var i = 0; i < sides.length; i ++ ) {

	var side = sides[ i ];

	var element = document.createElement( 'img' );
	element.width = side_len; // 2 pixels extra to close the gap.
	element.src = side.url;

	var object = new THREE.CSS3DObject( element );
	object.position.fromArray( side.position );
	object.rotation.fromArray( side.rotation );
	scene.add( object );
    }

    pointLight = new THREE.PointLight(0xFFFFFF);
    scene.add(pointLight);
    
    document.getElementById(canvasid).appendChild(renderer.domElement);

    document.getElementById(canvasid).addEventListener( 'mousedown', onDocumentMouseDown, false );

    document.getElementById(pan_lt).addEventListener( 'mousedown', function(e){pan_timer = setInterval(onSceneMoveLeft, 50)}, false );
    document.getElementById(pan_lt).addEventListener( 'mouseup', function(e){window.clearInterval(pan_timer)}, false );

    document.getElementById(pan_rt).addEventListener( 'mousedown', function(e){pan_timer = setInterval(onSceneMoveRight,50)}, false );
    document.getElementById(pan_rt).addEventListener( 'mouseup', function(e){window.clearInterval(pan_timer)}, false );

    document.getElementById(pan_up).addEventListener( 'mousedown', function(e){pan_timer = setInterval(onSceneMoveUp, 50)}, false );
    document.getElementById(pan_up).addEventListener( 'mouseup', function(e){window.clearInterval(pan_timer)}, false );

    document.getElementById(pan_down).addEventListener( 'mousedown', function(e){pan_timer = setInterval(onSceneMoveDown, 50)}, false );
    document.getElementById(pan_down).addEventListener( 'mouseup', function(e){window.clearInterval(pan_timer)}, false );
    
    document.getElementById(zoom_in).addEventListener( 'mousedown', onSceneZoomIn, false );
    document.getElementById(zoom_out).addEventListener( 'mousedown', onSceneZoomOut, false );

    document.addEventListener( 'keydown', onDocumentKeyDown, false );
    document.addEventListener( 'keypress', onDocumentKeyPress, false );
    document.addEventListener( 'keyup', onDocumentKeyUp, false );
    
//    document.getElementById(canvasid).addEventListener( 'mousewheel', onDocumentMouseWheel, false );

    document.getElementById(canvasid).addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.getElementById(canvasid).addEventListener( 'touchmove', onDocumentTouchMove, false );

    window.addEventListener( 'resize', onWindowResize, false );
}

function onWindowResize() {
    camera.aspect = getCanvasWidth(canvasid) / getCanvasHeight(canvasid);
    camera.updateProjectionMatrix();

    renderer.setSize( getCanvasWidth(canvasid), getCanvasHeight(canvasid) );
}

function render() {
    requestAnimationFrame(render);

    lat = Math.max( - 85, Math.min( 85, lat ) );
    phi = THREE.Math.degToRad( 90 - lat );
    theta = THREE.Math.degToRad( lon );
    
    focus.x = Math.sin( phi ) * Math.cos( theta );
    focus.y = Math.cos( phi );
    focus.z = Math.sin( phi ) * Math.sin( theta );

    camera.lookAt(focus);

    renderer.render(scene, camera);
}

function onDocumentMouseMove(event){
    var movementX = event.movementX || event.mozMovementX || event.webkitMovementX || 0;
    var movementY = event.movementY || event.mozMovementY || event.webkitMovementY || 0;

    lon -= movementX * 0.5;
    lat += movementY * 0.5;
    //http://threejs.org/examples/css3d_panorama.html
};

function onDocumentKeyDown(event){
//    event.preventDefault();
//    console.log(event.keyCode + "down");
    var angle = 5;
    switch(event.keyCode){
    case KEY_LEFT:
	lon -= angle;
	break;
    case KEY_UP:
	lat += angle;
	break;
    case KEY_RIGHT:
	lon += angle;
	break;
    case KEY_DOWN:
	lat -= angle;
	break;
    }

    //http://threejs.org/examples/css3d_panorama.html
};


function onSceneMoveUp(event){
    onDocumentKeyDown({keyCode: KEY_UP});
}

function onSceneMoveLeft(event){
    onDocumentKeyDown({keyCode: KEY_LEFT});
}
function onSceneMoveRight(event){
    onDocumentKeyDown({keyCode: KEY_RIGHT});
}
function onSceneMoveDown(event){
    onDocumentKeyDown({keyCode: KEY_DOWN});
}

function onDocumentKeyPress(event){
    //console.log(event.keyCode + "press");
};

function onDocumentKeyUp(event){
    //console.log(event.keyCode + "up");
};


function onDocumentMouseDown( event ) {
    event.preventDefault();
    document.body.addEventListener( 'mousemove', onDocumentMouseMove, false );
    document.body.addEventListener( 'mouseup', onDocumentMouseUp, false );
}

function onDocumentMouseUp( event ) {
    document.body.removeEventListener( 'mousemove', onDocumentMouseMove );
    document.body.removeEventListener( 'mouseup', onDocumentMouseUp );
}

function onDocumentMouseWheel( event ) {
    camera.fov -= event.wheelDeltaY * 0.05;
    camera.updateProjectionMatrix();
}


function onSceneZoomIn(){
    onDocumentMouseWheel({wheelDeltaY: ZOOM_DELTA});
}

function onSceneZoomOut(){
    onDocumentMouseWheel({wheelDeltaY: -ZOOM_DELTA});
}

function onDocumentTouchStart( event ) {
    event.preventDefault();

    var touch = event.touches[ 0 ];

    touchX = touch.screenX;
    touchY = touch.screenY;
}

function onDocumentTouchMove( event ) {
    event.preventDefault();

    var touch = event.touches[ 0 ];

    lon -= ( touch.screenX - touchX ) * 0.1;
    lat += ( touch.screenY - touchY ) * 0.1;

    touchX = touch.screenX;
    touchY = touch.screenY;
}

function Radar(parentid, id, lat, lon)
{
    this.lat = lat;
    this.lon = lon;
    this.id = id;
    this.parentid = parentid;

    this.put = function(containerid)
    {
	this.divid =  this.parentid + "_" + this.id;
	this.div = $("<div id=" + this.divid + ">"); //Equivalent: $(document.createElement('img'))
	this.div.appendTo('#' + containerid);
	this.div.css('position', 'absolute');
	this.div.css('left', this.lat + 'px');
	this.div.css('top', this.lon + 'px');

	this.image = $("<img>"); //Equivalent: $(document.createElement('img'))
	this.image.attr('src', '/get/scene/{{pv_username}}/{{pv_textid}}/{{pv_index}}/c');
	this.image.appendTo('#' + this.divid);
	this.image.attr('');
	return this.image;
    }
}

var radars = new Array();
var radar_count = {{ pv_radar_count }};
var radar_poss = {};

{% for p in pv_radar_poss %}
radar_poss.pos_{{ forloop.counter0 }} = {x: {{ p.x }}, y: {{ p.y }} }
{% endfor %}


{% for p in pv_radar_poss %}
radars[{{ forloop.counter0 }}] = new Radar(floorid, "{{ forloop.counter0 }}", radar_poss.pos_{{ forloop.counter0 }}.x, radar_poss.pos_{{ forloop.counter0 }}.y);
radars[{{ forloop.counter0 }}].put(floorid);
{% endfor %}

