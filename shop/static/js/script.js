$(document).ready(function() {
    var form = $('#rating_form');
    var voted = 0;
    var voted_now = 0;
    var user = form.data('user');
    var user_rating = form.data('user_rating');

    if (user_rating) {
        voted = 1;
        $('#your_rating').text("Ви вже голосували оцінка: "+user_rating);
        $('.rating-active').detach()
    }
    else if (!user) {
        $('#your_rating').text("Голосувати можуть лише зареєстровані користувачі");
    }
    else {
        var rating_width;
        var rating;
        $('.rating').on('click', function (e) {
            console.log('click');
            var data = {};
            data.click_rating = rating_width/32;
            var csrf_token = $('#rating_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
            var url = form.attr("action");


            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                    rating = data.r_rating;
                    var avg_rating = (Math.round(data.avg_rating*10)/10).toFixed(1)
                    voted_now = 1;
                    $('#product_avg_rating').text(avg_rating);
                    $('.avg').width(data.px_rating);
                    console.log(avg_rating)
                },

                error: function(){
                    console.log(data.user_rating);
                }
            });
            });
        function roundTo32(num) {
            return Math.round(num/32)*32;
        }

        $('.rating').mousemove(function(e){
            var rating_active = $('.rating-active');
            var pos = $(this).offset();
            var star_left = pos.left;
            rating_width = roundTo32(e.pageX - star_left);
            if (voted_now){

                $('#your_rating').text("Ви вже голосували оцінка: "+rating);
                $('.rating-active').addClass('hidden');
            }
            else {
                $('#active_rating').removeClass('hidden');
                rating_active.width(rating_width);
                $('.avg').addClass('hidden');
                $('#active_rating').text("Ваша оцінка: "+rating_width/32);
                rating_active.removeClass('hidden');
            }


        });



        $('.rating').mouseleave(function () {
            $('.avg').removeClass('hidden')
            $('.rating-active').addClass('hidden');
            $('#active_rating').addClass('hidden');
            }

        )
    }


});
