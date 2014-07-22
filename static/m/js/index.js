//<![CDATA[ 

$(function(){
    Friend = Backbone.Model.extend({
        //Create a model to hold friend atribute
        name: null
    });

    window.AppView = Backbone.View.extend({
        el: $("body"),
        events: {
            "click #add-friend":  "showPrompt",
            "mouseover .title_left_spot": "moveRight"
        },

	moveLeft: function(){
	    $("#main_container").css("left", "0px");
	},

        moveRight: function(){
	    if($("#main_container").css("left").localeCompare("0px") != 0){
		alert($("#main_container").css("left"));
		$("#main_container").css('left', 0);
	    }
            $("#main_container").css("left", "80%");              
        },
        showPrompt: function () {
            var friend_name = prompt("Who is your friend?");
            var friend_model = new Friend({ name: friend_name });
            this.friends.add( friend_model );
        },
        initialize: function () {
            this.friends = new Friends( null, { view: this });
            //Create a friends collection when the view is initialized.
            //Pass it a reference to this view to create a connection between the two
        },

        addFriendLi: function (model) {
            //The parameter passed is a reference to the model that was added
            $("#friends-list").append("<li>" + model.get('name') + "</li>");
            //Use .get to receive attributes of the model
        }

    });

    Friends = Backbone.Collection.extend({
        //This is our Friends collection and holds our Friend models
        initialize: function (models, options) {
            this.bind("add", options.view.addFriendLi);
            //Listen for new additions to the collection and call a view function if so
        }
    });
    var appview = new AppView;

});

//]]>  
