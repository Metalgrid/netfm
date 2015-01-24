$("#nav-back").click(function() {
    history.back();
});

$("#nav-forward").click(function() {
    history.forward();
});

$("#nav-refresh").click(function() {
    history.go(0);
});