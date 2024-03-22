$(document).ready(function(){
    $("#stream").hide();
    $("#course-reader").show();

    $("#course-read-menu-item").click(function (){
        $("#stream").hide();
        $("#course-reader").show(250);
    });

    $("#stream-menu-item").click(function (){
        $("#course-reader").hide();
        $("#stream").show(250);
    });
});