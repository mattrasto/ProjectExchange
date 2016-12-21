$(document).ready(function(){
	
	//One of the main topics is selected
	$(".navigationselect").click(function(){
		$(".navigationselect").css("color", "#3D3D3D");
		//Add each inner class if subsections are made under another main topic
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		
		if ($(this).val() == "BitSomething"){
			$(".aboutblockcontent").css("display", "none");
			$("#content1").css("display", "inline-block");
		}
		
		if ($(this).val() == "Bitcoin"){
			$(".aboutblockcontent").css("display", "none");
			$("#content8").css("display", "inline-block");
		}
		
		if ($(this).val() == "API"){
			$(".aboutblockcontent").css("display", "none");
			$("#content12").css("display", "inline-block");
		}
		
		if ($(this).val() == "Resources"){
			$(".aboutblockcontent").css("display", "none");
			$("#content13").css("display", "inline-block");
		}
	});
	
	//Anything under "BitSomething" or itself is selected
	$(".navigationselectinner1").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect1").css("color", "#7DABFF");
		
		if ($(this).val() == "Common Terms"){
			$(".aboutblockcontent").css("display", "none");
			$("#content2").css("display", "inline-block");
		}
		
		if ($(this).val() == "Basic Orders"){
			$(".aboutblockcontent").css("display", "none");
			$("#content3").css("display", "inline-block");
		}
		
		if ($(this).val() == "MTC's"){
			$(".aboutblockcontent").css("display", "none");
			$("#content4").css("display", "inline-block");
		}
		
		if ($(this).val() == "Loans"){
			$(".aboutblockcontent").css("display", "none");
			$("#content5").css("display", "inline-block");
		}
		
		if ($(this).val() == "Private Trades"){
			$(".aboutblockcontent").css("display", "none");
			$("#content6").css("display", "inline-block");
		}
		
		if ($(this).val() == "Petition System"){
			$(".aboutblockcontent").css("display", "none");
			$("#content7").css("display", "inline-block");
		}
	});
	
	//Anything under "Bitcoin" or itself is selected
	$(".navigationselectinner2").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect2").css("color", "#7DABFF");
		
		if ($(this).val() == "The Network"){
			$(".aboutblockcontent").css("display", "none");
			$("#content9").css("display", "inline-block");
		}
		
		if ($(this).val() == "The Blockchain"){
			$(".aboutblockcontent").css("display", "none");
			$("#content10").css("display", "inline-block");
		}
		
		if ($(this).val() == "Mining"){
			$(".aboutblockcontent").css("display", "none");
			$("#content11").css("display", "inline-block");
		}
	});
});