$(function(){

    var Product = Backbone.Model.extend({
	initialize: function (vendor, product_name, plan_name, offer) {
            this.vendor = vendor;
	    this.product_name = product_name;
	    this.plan_name = plan_name
            this.offer = offer;
	}
    });

    var Feature = Backbone.Model.extend({
	initialize: function(label, id, rest_url){
	    this.label = label;
	    this.id = id;
	    this.rest_url = url;
	}
    });

    
    var FeatureList = Backbone.Collection.extend(
	
    );

    var ProductList = Backbone.Collection.extend({
	model: Product,

	url: '/cloudchoice/products/',
    });

    var ProductView = Backbone.View.extend({
	tagName: 'li',
	template: _.template($('#product-list-template').html()),

	render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
	}
    });

    var FeatureView = Backbone.View.extend({
	tagName: 'li',
	className: "flat-li",
	template: _.template($('#feature-list-template').html()),
	render: function(){
            this.$el.html(this.template(this.model.toJSON()));
            return this;
	}
    });


//    var productList = new ProductList;


    
    var ProductListApp = Backbone.View.extend({
	el: $("#product-list-app-container"),

	events: {
	    "click #is-website": "select_website",
	},

	select_website: function(){alert(this);},
	
	initialize: function(){
	    this.productList = new ProductList;
	    this.featureList = new FeatureList;
	    
	    this.listenTo(this.productList, 'add', this.addOneProduct);
	    this.listenTo(this.featureList, 'add', this.addOneFeature);
	    this.productList.fetch();

	    this.featureList.add({label: 'Web site',       id: 'is_website',       rest_url: 'website'});
	    this.featureList.add({label: 'Virtual Server', id: 'is_virtualserver', rest_url: 'virtualserver'});
	    this.featureList.add({label: 'Application',    id: 'is_application',   rest_url: 'application'});
	},

	addOneFeature: function(feature){
	    var featureView = new FeatureView({model: feature});
	    $('#feature-list').append(featureView.render().$el);
	},
	
	addOneProduct: function(product){
	    var prdView = new ProductView({ model: product });
	    $("#product-list").append(prdView.render().$el);
	}
    });

    var productListApp = new ProductListApp;
});
