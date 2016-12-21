$(document).ready(function(){
	
	//One of the main topics is selected
	$(".navigationselect").click(function(){
		$(".navigationselect").css("color", "#3D3D3D");
		//Add each inner class if subsections are made under another main topic
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(".navigationselectinner3").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		
		if ($(this).val() == "Overview"){
			$(".accountblockcontent").css("display", "none");
			$("#content1").css("display", "inline-block");
		}
		
		if ($(this).val() == "Actions"){
			$(".accountblockcontent").css("display", "none");
			$("#content9").css("display", "inline-block");
		}
		
		if ($(this).val() == "Settings"){
			$(".accountblockcontent").css("display", "none");
			$("#content14").css("display", "inline-block");
		}
		
		if ($(this).val() == "Public Profile"){
			$(".accountblockcontent").css("display", "none");
			$("#content18").css("display", "inline-block");
		}
	});
	
	//Anything under "Overview" or itself is selected
	$(".navigationselectinner1").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(".navigationselectinner3").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect1").css("color", "#7DABFF");
		
		if ($(this).val() == "Balances"){
			$(".accountblockcontent").css("display", "none");
			$("#content2").css("display", "inline-block");
		}
		
		if ($(this).val() == "Open Basic Orders"){
			$(".accountblockcontent").css("display", "none");
			$("#content3").css("display", "inline-block");
		}
		
		if ($(this).val() == "Current MTC's"){
			$(".accountblockcontent").css("display", "none");
			$("#content4").css("display", "inline-block");
		}
		
		if ($(this).val() == "Current Loans"){
			$(".accountblockcontent").css("display", "none");
			$("#content5").css("display", "inline-block");
		}
		
		if ($(this).val() == "Open Private Trades"){
			$(".accountblockcontent").css("display", "none");
			$("#content6").css("display", "inline-block");
		}
		
		if ($(this).val() == "History"){
			$(".accountblockcontent").css("display", "none");
			$("#content7").css("display", "inline-block");
		}
		
		if ($(this).val() == "Statistics"){
			$(".accountblockcontent").css("display", "none");
			$("#content8").css("display", "inline-block");
		}
	});
	
	//Anything under "Actions" or itself is selected
	$(".navigationselectinner2").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(".navigationselectinner3").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect2").css("color", "#7DABFF");
		
		if ($(this).val() == "Make a Deposit"){
			$(".accountblockcontent").css("display", "none");
			$("#content10").css("display", "inline-block");
		}
		
		if ($(this).val() == "Make a Withdrawal"){
			$(".accountblockcontent").css("display", "none");
			$("#content11").css("display", "inline-block");
		}
		
		if ($(this).val() == "Bank Information"){
			$(".accountblockcontent").css("display", "none");
			$("#content12").css("display", "inline-block");
		}
		
		if ($(this).val() == "Open a Support Ticket"){
			$(".accountblockcontent").css("display", "none");
			$("#content13").css("display", "inline-block");
		}
	});
	
	//Anything under "Settings" or itself is selected
	$(".navigationselectinner3").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(".navigationselectinner3").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect3").css("color", "#7DABFF");
		
		if ($(this).val() == "Preferences"){
			$(".accountblockcontent").css("display", "none");
			$("#content15").css("display", "inline-block");
		}
		
		if ($(this).val() == "Update Account"){
			$(".accountblockcontent").css("display", "none");
			$("#content16").css("display", "inline-block");
		}
		
		if ($(this).val() == "Default Behaviors"){
			$(".accountblockcontent").css("display", "none");
			$("#content17").css("display", "inline-block");
		}
	});
	
	//Anything under "Public Profile" or itself is selected
	$(".navigationselectinner4").click(function(){
		$(".navigationselectinner1").css("color", "#3D3D3D");
		$(".navigationselectinner2").css("color", "#3D3D3D");
		$(".navigationselectinner3").css("color", "#3D3D3D");
		$(this).css("color", "#7DABFF");
		$(".navigationselect").css("color", "#3D3D3D");
		$("#navigationselect4").css("color", "#7DABFF");
	});
});