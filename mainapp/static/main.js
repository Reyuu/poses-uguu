var obj = "";
var tid = "";
var current_timeout = 0;
var timer = 0;
$("#spinner").hide();
function get_pose(){
    $.get("get_random_pose", function(data, status){
        //console.log(data["content_src"]);
            obj = data;
            $("#spinner").show()
            $("#pose").attr('src', obj["content_src"]).on('load', function(){
                $("#spinner").hide();
                
            })
        });
    
}

function jsUcfirst(s) 
        {
            //console.log(s);
            return s.charAt(0).toUpperCase() + s.slice(1);
        }

// set timeout

function repeat_forever() {
// do some stuff...
    get_pose();
    tid = setTimeout(repeat_forever, 1000*current_timeout); // repeat myself
}

function abortTimer() { // to be called when you want to stop the timer
    clearTimeout(tid);
}

$(function(){

    get_pose();

    $("#change-button").click(get_pose);
    $("#url-button").click(function(){
        window.open(obj["url"]);
    });
    $("#start-timer").click(function(){
        console.log(current_timeout);
        if (tid==""){
            current_timeout = $("#time-select").val();
            $(this).text("Stop timed!");
            console.log(current_timeout);
            tid = setTimeout(repeat_forever, 1000*current_timeout);

        }
        else{
            abortTimer();
            current_timeout = 0;
            $(this).text("Start timed!");
            tid = "";
        }
    });
})
