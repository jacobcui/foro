var camera, scene, renderer, focus;
var canvas;
var lon = 0, lat = 0;
var phi = 0, theta = 0;
var pointLight, light;

init();
render();

function getCanvasWidth(){
    return window.innerWidth;
}

function getCanvasHeight(){
    return window.innerHeight - 40;
}

function init(){
// set the scene size
    var side_len = getCanvasWidth();// 1125;
    var center_distance = side_len / 2.0;

// set some camera attributes
    VIEW_ANGLE = 60;  NEAR = 0.1;    FAR = 10000;

    camera = new THREE.PerspectiveCamera(VIEW_ANGLE, getCanvasWidth() / getCanvasHeight(), NEAR, FAR);
    scene = new THREE.Scene();
    scene.add(camera);     // add the camera to the scene

    renderer = new THREE.CSS3DRenderer();
    renderer.setSize(getCanvasWidth(), getCanvasHeight());

    focus = new THREE.Vector3( 0, 0, -center_distance );
    
    var name = 'dz';
//    var name = 'blank';
    
    var sides = [
	{
	    url: '/resource/image/vi/' + name + '_full/full_r/9/0_0.jpg',
	    position: [ -center_distance, 0, 0 ],
	    rotation: [ 0, Math.PI / 2, 0 ]
	},
	{
	    url: '/resource/image/vi/' + name + '_full/full_l/9/0_0.jpg',
	    position: [ center_distance, 0, 0 ],
	    rotation: [ 0, -Math.PI / 2, 0 ]
	},
	{
	    url: '/resource/image/vi/' + name + '_full/full_u/9/0_0.jpg',
	    position: [ 0,  center_distance, 0 ],
	    rotation: [ Math.PI / 2, 0, Math.PI ]
	},
	{
	    url: '/resource/image/vi/' + name + '_full/full_d/9/0_0.jpg',
	    position: [ 0, -center_distance, 0 ],
	    rotation: [ - Math.PI / 2, 0, Math.PI ]
	},
	{
	    url: '/resource/image/vi/' + name + '_full/full_f/9/0_0.jpg',
	    position: [ 0, 0,  center_distance ],
	    rotation: [ 0, Math.PI, 0 ]
	},
	{
	    url: '/resource/image/vi/' + name + '_full/full_b/9/0_0.jpg',
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
    
    document.getElementById('canvas').appendChild(renderer.domElement);

    document.getElementById('canvas').addEventListener( 'mousedown', onDocumentMouseDown, false );
    document.addEventListener( 'keydown', onDocumentKeyDown, false );
    document.addEventListener( 'keypress', onDocumentKeyPress, false );
    document.addEventListener( 'keyup', onDocumentKeyUp, false );
    
    document.getElementById('canvas').addEventListener( 'mousewheel', onDocumentMouseWheel, false );

    document.getElementById('canvas').addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.getElementById('canvas').addEventListener( 'touchmove', onDocumentTouchMove, false );

    window.addEventListener( 'resize', onWindowResize, false );
}

function onWindowResize() {
    camera.aspect = getCanvasWidth() / getCanvasHeight();
    camera.updateProjectionMatrix();

    renderer.setSize( getCanvasWidth(), getCanvasHeight() );
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

    lon -= movementX * 0.1;
    lat += movementY * 0.1;
    //http://threejs.org/examples/css3d_panorama.html
};

function onDocumentKeyDown(event){
//    event.preventDefault();
//    console.log(event.keyCode + "down");
    var angle = 5;
    switch(event.keyCode){
    case 37: // left
	lon -= angle;
	break;
    case 38: // up
	lat += angle;
	break;
    case 39: // right
	lon += angle;
	break;
    case 40: // down
	lat -= angle;
	break;
    }

    //    lon -= movementX * 0.1;
//    lat += movementY * 0.1;
    //http://threejs.org/examples/css3d_panorama.html
};

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
