$(document).ready(function () {
    console.log("now");
    $("#hidden").hide().css({visibility: "visible"}).fadeIn(1800);
});


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
        window.location.replace("https://checkers-vs-computer.herokuapp.com/usermove");
      }
      timeoutPoll = setTimeout(doPoll,2000);
    });
}


var dots = window.setInterval( function() {
    var wait = document.getElementById("waitingDots");
    if ( wait.innerHTML.length > 2 )
        wait.innerHTML = "";
    else
        wait.innerHTML += ".";
    }, 300);
