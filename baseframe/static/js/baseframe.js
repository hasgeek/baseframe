// Baseframe JS
$(function(){
    // Make alerts closable
    $(".alert-box").delegate("a.close", "click", function(event) {
    event.preventDefault();
        $(this).closest(".alert-box").fadeOut(function(event){
            $(this).remove();
        });
    });
});
