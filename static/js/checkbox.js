$(document).ready(function(){
    $(document).on("click", "#sample_data tbody .select-checkbox", function(){

        $("#phone").val("");
        if ($(this).parent().attr("class").indexOf("selected") > -1){
            let tel = $(this).next().next().next().html();
            $("#phone").val(tel);
        }

    });
});