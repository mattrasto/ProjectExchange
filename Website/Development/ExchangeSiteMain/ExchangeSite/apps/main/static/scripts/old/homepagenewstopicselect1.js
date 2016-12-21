$(document).ready(function(){
	
	$(".newsselect").click(function(){
		$(".newsselect").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		
		if ($(this).val() == "Statement"){
			$(".newsblockcontent").css("display", "none");
			$("#content3").css("display", "inline-block");
		}
		
		if ($(this).val() == "Welcome"){
			$(".newsblockcontent").css("display", "none");
			$("#content4").css("display", "inline-block");
		}
	});
});