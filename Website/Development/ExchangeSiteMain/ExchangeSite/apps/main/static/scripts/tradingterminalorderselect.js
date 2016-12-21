$(document).ready(function(){
    $("#instantorder").mouseover(function(){
    	//Controls order selection and form/condition setting
    	$("#ordercontent").animate({height: 421});
    	$(".orderbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$(".ordercontentcondition").css("display", "none");
    	$(".ordercontentconditionvalue").css("display", "none");
    	$(".ordertype").text("an Instant Order");
    	$(".createorderbutton").css("width", "250");
    	$(".createorderbutton").attr("value", "Place Instant Order");
    	$(".order_type").attr("value", "INSTANT");
    	$(".pricespan").html("Desired Total");
    	$(".volumespan").html("Desired Volume");
    	//Controls instant order checkboxes
    	$(".checkboxes").css("display", "block");
    	$(".ordercontentprice1").css("opacity", ".25");
    	$(".ordercontentprice1 input").prop('disabled', true);
    	$(".ordercontentvolume1").css("opacity", ".25");
    	$(".ordercontentvolume1 input").prop('disabled', true);
    	$(".ordercontentprice2").css("opacity", ".25");
    	$(".ordercontentprice2 input").prop('disabled', true);
    	$(".ordercontentvolume2").css("opacity", ".25");
    	$(".ordercontentvolume2 input").prop('disabled', true);
    	//Resets input fields when switching order types to prevent hidden values
    	$(".ordercontentprice1 input").val("");
    	$(".ordercontentprice2 input").val("");
    	$(".ordercontentvolume1 input").val("");
    	$(".ordercontentvolume2 input").val("");
    	$(".ordercontentcondition input").val("");
    	$(".ordercontentconditionvalue input").val("");
    });
    
    $("#liquidorder").mouseover(function(){
    	//Controls order selection and form/condition setting
    	$("#ordercontent").animate({height: 421});
    	$(".orderbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$(".ordercontentcondition").css("display", "none");
    	$(".ordercontentconditionvalue").css("display", "none");
    	$(".ordertype").text("a Liquid Order");
    	$(".createorderbutton").css("width", "250");
    	$(".createorderbutton").attr("value", "Place Liquid Order");
    	$(".order_type").attr("value", "LIQUID")
    	$(".pricespan").html("Price Per Unit")
    	$(".volumespan").html("Volume of Order")
    	//Controls instant order checkboxes
    	$(".checkboxes").css("display", "none")
    	$(".ordercontentprice1").css("opacity", "1");
    	$(".ordercontentprice1 input").prop('disabled', false);
    	$(".ordercontentvolume1").css("opacity", "1");
    	$(".ordercontentvolume1 input").prop('disabled', false);
    	$(".ordercontentprice2").css("opacity", "1");
    	$(".ordercontentprice2 input").prop('disabled', false);
    	$(".ordercontentvolume2").css("opacity", "1");
    	$(".ordercontentvolume2 input").prop('disabled', false);
    	//Resets input fields when switching order types to prevent hidden values
    	$(".ordercontentprice1 input").val("");
    	$(".ordercontentprice2 input").val("");
    	$(".ordercontentvolume1 input").val("");
    	$(".ordercontentvolume2 input").val("");
    	$(".ordercontentcondition input").val("");
    	$(".ordercontentconditionvalue input").val("");
    });
    
    $("#limitorder").mouseover(function(){
    	//Controls order selection and form/condition setting
    	$("#ordercontent").animate({height: 421});
    	$(".orderbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$(".ordercontentcondition").css("display", "none");
    	$(".ordercontentconditionvalue").css("display", "none");
    	$(".ordertype").text("a Limit Order");
    	$(".createorderbutton").css("width", "250");
    	$(".createorderbutton").attr("value", "Place Limit Order");
    	$(".order_type").attr("value", "LIMIT")
    	$(".pricespan").html("Price Per Unit")
    	$(".volumespan").html("Volume of Order")
    	//Controls instant order checkboxes
    	$(".checkboxes").css("display", "none")
    	$(".ordercontentprice1").css("opacity", "1");
    	$(".ordercontentprice1 input").prop('disabled', false);
    	$(".ordercontentvolume1").css("opacity", "1");
    	$(".ordercontentvolume1 input").prop('disabled', false);
    	$(".ordercontentprice2").css("opacity", "1");
    	$(".ordercontentprice2 input").prop('disabled', false);
    	$(".ordercontentvolume2").css("opacity", "1");
    	$(".ordercontentvolume2 input").prop('disabled', false);
    	//Resets input fields when switching order types to prevent hidden values
    	$(".ordercontentprice1 input").val("");
    	$(".ordercontentprice2 input").val("");
    	$(".ordercontentvolume1 input").val("");
    	$(".ordercontentvolume2 input").val("");
    	$(".ordercontentcondition input").val("");
    	$(".ordercontentconditionvalue input").val("");
    });
    
    $("#conditionalorder").mouseover(function(){
    	//Controls order selection and form/condition setting
    	$("#ordercontent").animate({height: 537});
    	$(".orderbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$(".ordercontentcondition").css("display", "inline");
    	$(".ordercontentconditionvalue").css("display", "inline");
    	$(".ordertype").text("a Conditional Order");
    	$(".createorderbutton").css("width", "300");
    	$(".createorderbutton").attr("value", "Place Conditional Order");
    	$(".order_type").attr("value", "CONDITIONAL")
    	$(".pricespan").html("Price Per Unit")
    	$(".volumespan").html("Volume of Order")
    	//Controls instant order checkboxes
    	$(".checkboxes").css("display", "none")
    	$(".ordercontentprice1").css("opacity", "1");
    	$(".ordercontentprice1 input").prop('disabled', false);
    	$(".ordercontentvolume1").css("opacity", "1");
    	$(".ordercontentvolume1 input").prop('disabled', false);
    	$(".ordercontentprice2").css("opacity", "1");
    	$(".ordercontentprice2 input").prop('disabled', false);
    	$(".ordercontentvolume2").css("opacity", "1");
    	$(".ordercontentvolume2 input").prop('disabled', false);
    	//Resets input fields when switching order types to prevent hidden values
    	$(".ordercontentprice1 input").val("");
    	$(".ordercontentprice2 input").val("");
    	$(".ordercontentvolume1 input").val("");
    	$(".ordercontentvolume2 input").val("");
    	$(".ordercontentcondition input").val("");
    	$(".ordercontentconditionvalue input").val("");
    });
    
    //Controls instant order input fields based on checkboxes
	$(".ordercontentprice1").css("opacity", ".25");
	$(".ordercontentprice1 input").prop('disabled', true);
	$(".ordercontentvolume1").css("opacity", ".25");
	$(".ordercontentvolume1 input").prop('disabled', true);
	$(".ordercontentprice2").css("opacity", ".25");
	$(".ordercontentprice2 input").prop('disabled', true);
	$(".ordercontentvolume2").css("opacity", ".25");
	$(".ordercontentvolume2 input").prop('disabled', true);
    
	//If buy order price checkbox is checked
    $("#pricecheckbox1").click(function() {
	    if ($('#pricecheckbox1').is(":checked")) {
			$(".ordercontentprice1").css("opacity", "1");
			$(".ordercontentprice1 input").prop('disabled', false);
			$(".ordercontentvolume1").css("opacity", ".25");
			$(".ordercontentvolume1 input").prop('disabled', true);
			$("#buy_order_constraint").attr("value", "PRICE");
			$(".ordercontentprice1 input").val("");
	    	$(".ordercontentprice2 input").val("");
	    	$(".ordercontentvolume1 input").val("");
	    	$(".ordercontentvolume2 input").val("");
	    	$(".ordercontentcondition input").val("");
	    	$(".ordercontentconditionvalue input").val("");
		};
    });
    
    //If buy order volume checkbox is checked
    $("#volumecheckbox1").click(function() {
		if ($("#volumecheckbox1").is(":checked")) {
			$(".ordercontentprice1").css("opacity", ".25");
			$(".ordercontentprice1 input").prop('disabled', true);
			$(".ordercontentvolume1").css("opacity", "1");
			$(".ordercontentvolume1 input").prop('disabled', false);
			$("#buy_order_constraint").attr("value", "VOLUME");
			$(".ordercontentprice1 input").val("");
	    	$(".ordercontentprice2 input").val("");
	    	$(".ordercontentvolume1 input").val("");
	    	$(".ordercontentvolume2 input").val("");
	    	$(".ordercontentcondition input").val("");
	    	$(".ordercontentconditionvalue input").val("");
		};
    });
    
    //If sell order price checkbox is checked
    $("#pricecheckbox2").click(function() {
	    if ($('#pricecheckbox2').is(":checked")) {
			$(".ordercontentprice2").css("opacity", "1");
			$(".ordercontentprice2 input").prop('disabled', false);
			$(".ordercontentvolume2").css("opacity", ".25");
			$(".ordercontentvolume2 input").prop('disabled', true);
			$("#sell_order_constraint").attr("value", "PRICE");
			$(".ordercontentprice1 input").val("");
	    	$(".ordercontentprice2 input").val("");
	    	$(".ordercontentvolume1 input").val("");
	    	$(".ordercontentvolume2 input").val("");
	    	$(".ordercontentcondition input").val("");
	    	$(".ordercontentconditionvalue input").val("");
		};
    });
    
    //If sell order volume checkbox is checked
    $("#volumecheckbox2").click(function() {
		if ($("#volumecheckbox2").is(":checked")) {
			$(".ordercontentprice2").css("opacity", ".25");
			$(".ordercontentprice2 input").prop('disabled', true);
			$(".ordercontentvolume2").css("opacity", "1");
			$(".ordercontentvolume2 input").prop('disabled', false);
			$("#sell_order_constraint").attr("value", "VOLUME");
			$(".ordercontentprice1 input").val("");
	    	$(".ordercontentprice2 input").val("");
	    	$(".ordercontentvolume1 input").val("");
	    	$(".ordercontentvolume2 input").val("");
	    	$(".ordercontentcondition input").val("");
	    	$(".ordercontentconditionvalue input").val("");
		};
    });
});