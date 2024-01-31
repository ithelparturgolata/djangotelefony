$(document).ready(function(){
        $(document).on("dblclick", "#sample_data tbody .select-checkbox", function(){
        let tel = $(this).next().next().next().html();
        $("#phone").val('');

    });
});