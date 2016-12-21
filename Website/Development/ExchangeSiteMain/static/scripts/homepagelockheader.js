function lock() {
    if(document.getElementById("lockbutton").value=="Lock"){
        document.getElementById("lockbutton").value="Unlock";
        document.getElementById("header").style.position="static";
        menubar = document.getElementById("menubar");
        menubar.style.position="static";
        menubar.style.margin="0px";
        menubar.style.width="100%";
        underbody = document.getElementById("underbody");
        underbody.style.paddingTop="0px";
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
        console.log("Left: " + menubar.style.marginLeft);
        console.log("Right: " + menubar.style.marginRight);
        menubar.style.width="85%";
        underbody = document.getElementById("underbody");
        underbody.style.paddingTop="86px";
        underbody.style.marginTop="0px";
        console.log("Run 2");
    }
}