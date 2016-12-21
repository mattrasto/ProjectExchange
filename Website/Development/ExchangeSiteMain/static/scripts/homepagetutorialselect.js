$(document).ready(function(){
    $("#tutorial1").mouseover(function(){
    	$("#tutorialcontent").animate({height: "364"});
    	$(".tutorialbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$("#tutorialcontent").html("<h1>A Financial Transformation</h1>" +
    							   "<p>Bitcoin was the first cryptocurrency; that is, a digitally stored currency. " +
	                               "It's stored on computers, like any other piece of data, and can be transferred " +
	                               "anywhere in the world for less fees than a credit card. It's based on a protocol called the &quot;Blockchain,&quot; which is " +
	                               "a registry of all transactions ever conducted. This enables Bitcoin, and " +
	                               "its other cryptocurrency children, to be a safer, faster, and more reliable way to pay and store value.</p>");
    });
    
    $("#tutorial2").mouseover(function(){
    	$("#tutorialcontent").animate({height: "464"});
    	$(".tutorialbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$("#tutorialcontent").html("<h1>Power and Security: The Blockchain</h1>" +
    							   "<p>By using cryptography, a way to encode data into unrecognizable pieces, cryptocurrency is able to make itself both safe and self-regulating. " +
	                                "Every time a transaction is made, the network of &quot;Miners&quot;, which are just computers that solve difficult math problems for network maintenance, " +
	                                "confirms the transaction and records it in the Blockchain, which is then shared across all users on the entire cryptocurrency network. " +
	                                "It sounds complex, but all this means is that when you send a unit of cryptocurrency, for example 1 Bitcoin, " +
	                                "every user has a copy of your transaction, so it can't be copied, edited, or erased.</p>");
    });
    
    $("#tutorial3").mouseover(function(){
    	$("#tutorialcontent").animate({height: "604"});
    	$(".tutorialbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$("#tutorialcontent").html("<h1>Faster, Smarter, and Promising</h1>" +
				    			   "<p>There are multiple reasons why cryptocurrency is so useful. Due to its digital background, " +
				                   "it's a natural candidate for online shopping. Imagine paying for an item on a website, and having the payment processed without " +
				                   "any middleman that charges fees and could refuse your transaction. The technology behind it, particularly the Blockchain, " +
				                   "is also perfect ground upon which multiple other technologies could be built. Decentralization is a powerful tool, " +
				                   "and could be applied to many other industries within the world.</p><br>" +
				                   "<p>To learn more about Bitcoin, please see our more extensive tutorial in the &quot;About&quot; section or visit the official Bitcoin website: www.Bitcoin.org</p>");
    });
    
    $("#tutorial4").mouseover(function(){
    	$("#tutorialcontent").animate({height: "514"});
    	$(".tutorialbutton").css("background-color", "#EBEBEB");
    	$(this).css("background-color", "#7DABFF");
    	$("#tutorialcontent").html("<h1>More for You, Less for Us</h1>" +
				    			   "<p>BitSomething was made to represent the true movement of Bitcoin: power to the people. " +
				                   "We believe that the user should be the one that controls their finances, and we didn't find that with any " +
				                   "other exchanges. This exchange was not intended to just be a medium for introducing members to cryptocurrency, " +
				                   "but also to give the user all of the tools that they want and need. We offer multiple trading strategies, including regular buying and selling, " +
				                   "flexible loaning techniques, and user-to-user trading. In the future, we intend to improve and develop the exchange into a place where anything " +
				                   "that you dream up can be implemented by our team, and maintained with our best service. Go ahead and register to try BitSomething out; we guarantee you'll like it!</p>");
    });
});