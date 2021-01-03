function myFunc(vars) {
  if(vars === "startedThink"){
    console.log("computer started thinking b");
    doPoll();
  }
}

function doPoll(){
     requestForEnd = $.post('/compdone/',
     function(data) {
      console.log("checked now");
      console.log(data);
      if (data == "DONE"){
        console.log(data);
        window.location.replace("http://localhost:5000/usermove");
      }
      timeoutPoll = setTimeout(doPoll,2000);
    });
}


var dots = window.setInterval( function() {
    var wait = document.getElementById("waitingDots");
    console.log("ag");
    if ( wait.innerHTML.length > 2 )
        wait.innerHTML = "";
    else
        wait.innerHTML += ".";
    }, 300);
