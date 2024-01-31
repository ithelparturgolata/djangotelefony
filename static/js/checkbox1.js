$(document).ready(function(){
    $(document).on("click", "#sample_data tbody .select-checkbox", function(){
        let tel = $(this).next().next().next().next().html();
        $("#phone").val(tel);
    });
});

