function lock() {
    if(document.getElementById("lockbutton").value=="Lock"){
        document.getElementById("lockbutton").value="Unlock";
        document.getElementById("header").style.position="static";
        menubar = document.getElementById("menubar");
        menubar.style.position="static";
        menubar.style.margin="0px";
        menubar.style.width="100%";
        underbody = document.getElementById("underbody");
        underbody.style.paddingTop="30px";
        underbody.style.marginTop="-5px";
        console.log("Run 1");
    }
    
    else if(document.getElementById("lockbutton").value=="Unlock"){
        document.getElementById("lockbutton").value="Lock";
        document.getElementById("header").style.position="fixed";
        menubar = document.getElementById("menubar");
        menubar.style.position="fixed";
        menubar.style.marginLeft="7.5%";
        menubar.style.marginRight="7.5%";
        menubar.style.width="85%";
        underbody = document.getElementById("underbody");
        underbody.style.paddingTop="116px";
        underbody.style.marginTop="0px";
        console.log("Run 2");
    }
}