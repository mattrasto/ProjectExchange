$(document).ready(function(){
	
	x = 1;
	
	$(".newsselect").click(function(){
		
		console.log(x);
		
		if (x > 1) {
			//console.log("Old element before assign:")
			//console.log(oldelement)
			//console.log("Old color before assign: " + oldcolor)
			//console.log("New color before assign: " + newcolor);
			oldelement.css("color", oldcolor);
			console.log("Done");
		};
		
		oldelement = $(this);
		oldcolor = $(this).css("color");
		newcolor = "#7DABFF";
		
		//console.log("Old element after assign:")
		//console.log(oldelement)
		//console.log("Old color after assign: " + oldcolor)
		//console.log("New color after assign: " + newcolor);
		
		x = x + 1;
		
		//$(".newsselect").css("color", "#3D3D3D");
		$(this).css("color", newcolor);
		
		
		
		if ($(this).val() == "Welcome"){
			$(".newsblockcontent").css("display", "none");
			$("#Welcome").css("display", "inline-block");
		}
		
		else if ($(this).val() == "Statement"){
			$(".newsblockcontent").css("display", "none");
			$("#Statement").css("display", "inline-block");
		}
		
		else {
		
			story_id = $(this).attr("id");
			//console.log("Story ID: ");
			//console.log(story_id);
			content_id = story_id.slice(5);
			//console.log("Content ID: ");
			//console.log(content_id);
			
			$(".newsblockcontent").css("display", "none");
			$("#content" + content_id).css("display", "inline-block");
		}
	});
});