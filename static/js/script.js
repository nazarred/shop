$(document).ready(function() {
    var form = $('#rating_form');
    console.log(form);
    form.on('click', function (e) {
        e.preventDefault();
        console.log('123');
        var rating = $('#id_rating').val();
        console.log(rating);
        var form_data = $('#rating_form');
        var product_id = form_data.data('product_id');
        console.log(product_id);


            var data = {};
            data.product_id = product_id;
            data.rating = rating;
            var csrf_token = $('#rating_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
            var url = form.attr("action");


            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                    console.log("OK");
                },

                error: function(){
                    console.log("error")
                }
            });
    });



    $('.vote-hover').mouseover(function(){
        console.log('123');
        $('.vote-now').removeClass('hidden');
        
    })


});
