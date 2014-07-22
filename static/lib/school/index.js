
var schoolList;

function debugDisplay(text){
    text = JSON.stringify(text);
    $("#debug").html($("#debug").html() + "<BR>" + text);
}

var map;

var infowindow;

function mapMarker(school) {
    var marker = new google.maps.Marker({
        map: map,
        position: school.loc,
//	draggable:true,
	animation: google.maps.Animation.DROP
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent("<B>" + school.name + "</B>" + "<BR>" + school.address + "<BR>" + "Rank: " + school.rank);
        infowindow.open(map, this);
    });
}

$(function(){
    $('input:text, input:password, input[type=email]')
	.button().addClass('input');


})