$(document).ready(function(){
    $("#stream").hide();
    $("#editor").hide();
    $("#course-reader").show();

    $("#course-read-menu-item").click(function (){
        $("#stream").hide();
        $("#editor").hide();
        $("#course-reader").show(250);
    });

    $("#stream-menu-item").click(function (){
        $("#course-reader").hide();
        $("#editor").hide();
        $("#stream").show(250);
    });

    $("#editor-menu-item").click(function () {
        $("#course-reader").hide();
        $("#stream").hide();
        $("#editor").show(250);
    });
});