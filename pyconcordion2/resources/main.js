$(function() {
  $(".stackTraceButton").on("click", function(event) {
    $(".stackTrace." + $(this).data("exception-index")).toggle();
  })
});
