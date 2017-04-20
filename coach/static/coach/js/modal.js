// Modal

// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    document.getElementById('voiceRecordStatus').value = "";
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        document.getElementById('voiceRecordStatus').value = "";
        modal.style.display = "none";
    }
}

function modal_function(svg, x0, mouseX, mouseY, imageOffsetX, imageOffsetY){
    
    // Showing the marked distance to the user
    document.getElementById('textinput-1').value = String(x0) + ' km';

    // Corresponding latitude and longitude of the marked distance

    // Voice recording feature
    $( "#voiceRecorded" ).one ("click", function() {
        document.getElementById('voiceRecordStatus').value = "Recording...";
        console.log("voiceRecording url: " + voiceRecording);
        $.ajax({
            type: "GET",
            url: voiceRecording,
            success: function(){
                document.getElementById('voiceRecordStatus').value = "Voice successfully recorded";
            }
        });
    });

    // Voice playing feature
    $( "#voicePlayed" ).one ("click", function() {
        $.ajax({
            type: "GET",
            url: voicePlaying,
            success: function(data){
                var snd = new Audio(data['url']); // Works perfectly :)))
                snd.play();
            }
        });
    });

    // Voice saving feature
    $( "#voiceSaved" ).one ("click", function() {
        console.log("Trying to disable the button");
        console.log($(this).prop('disabled'));
        $(this).prop('disabled', true); // NOTE: http://stackoverflow.com/questions/11705337/javascript-jquery-disable-submit-button-on-click-prevent-double-submitting
        console.log($(this).prop('disabled'));
        for (var i=0; i<gpx_distance.length; i++){
            if (x0 <= gpx_distance[i]){
                var dis_Mark_Pos = i;
                break;
            }
        }
        var dis_Mark = x0;
        var dis_lat = gpx_latitude[dis_Mark_Pos];
        var dis_lon = gpx_longitude[dis_Mark_Pos];
        alert("Voice saved");
        data = {dis_Mark: dis_Mark, dis_Mark_Pos: dis_Mark_Pos, dis_lat: dis_lat, dis_lon: dis_lon, csrfmiddlewaretoken : getCookie('csrftoken')};
        $.post(voiceSaving, data, function(response){
        });

        document.getElementById('voiceRecordStatus').value = "";
        modal.style.display = "none";
        // Identify latitude, lingitude corresponding to x0
        saveAudio(x0);
        addSoundIcon(x0); 
    });
}