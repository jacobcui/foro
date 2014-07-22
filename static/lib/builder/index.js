$(function() {
    $( "#itemlabel" ).draggable().click();
    $( "#itemtextinput" ).draggable().click();
    $( "#droppable" ).droppable({
	accept: ".draggable",
	activeClass: "ui-state-highlight",
	hoverClass: "ui-state-active",
	drop: function( event, ui ) {
            $( this )
		.find( "p" )
		.html( "Dropped!" );
	}
    });
});

