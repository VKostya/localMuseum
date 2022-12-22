$(function () {
    $("#autocomplete").autocomplete({
        source: "/api/museums/autocomplete"
    });
});