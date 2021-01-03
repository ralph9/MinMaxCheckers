function myFunc(vars) {
  if(vars === "startedThink"){
    console.log("computer thinking");
    doPoll();
  }
}

var requestForEnd;
var timeoutPoll;

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

function abortRequest(){
  console.log("aborting polling now");
  clearTimeout(timeoutPoll);
  // console.log(requestForEnd);
  // requestForEnd.abort();
}
