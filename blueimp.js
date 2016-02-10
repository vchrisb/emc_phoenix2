load_pictures()
function load_pictures() {
//'use strict';
$.ajax({
    url: 'http://127.0.0.1:8000/api/tweetpic/',
    type : "GET", // http method
    dataType: 'json'
}).done(function (result) {
    $.each(result.photo, function (index, photo) {
      console.log(photo.url)
    });
};
