$(document).ready(function () {
    $("#hidden").hide().css({visibility: "visible"}).fadeIn(1800);
    if($("#hidden").text().charAt(0) === "M"){
      $("#hidden").css({color: "red"}).delay(3000);
      /*setTimeout(
        function(){$("#hidden").css({color: "black"});
      }, 1500);
      */
    }
});

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
        window.location.replace("https://checkers-vs-computer.herokuapp.com/usermove");
      }
      timeoutPoll = setTimeout(doPoll,2000);
    });
}

function abortRequest(){
  console.log("aborting polling now");
  clearTimeout(timeoutPoll);
}


jQuery(document).ready(function()
{
    jQuery('input').each(function()
    {
        if (jQuery(this).attr('placeholder') && jQuery(this).attr('placeholder') != '')
        {
            jQuery(this).attr( 'data-placeholder', jQuery(this).attr('placeholder') );
        }
    });
    jQuery('input').focus(function()
    {
        if (jQuery(this).attr('data-placeholder') && jQuery(this).attr('data-placeholder') != '')
        {
            jQuery(this).attr('placeholder', '');
        }
    });
    jQuery('input').blur(function()
    {
        if (jQuery(this).attr('data-placeholder') && jQuery(this).attr('data-placeholder') != '')
        {
            jQuery(this).attr('placeholder', jQuery(this).attr('data-placeholder'));
        }
    });
});
