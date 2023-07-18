$( function(){
    $( "#autocomplete" ).autocomplete({
        classes: {"ui-autocomplete":"bg-dark container card shadow text-white mb-3"},
        source: "/user/autocomplete",
    });
});
