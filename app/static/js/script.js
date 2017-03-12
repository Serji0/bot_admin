$(function () {
    function validateForm() {
        $('.text-error').remove();
        var v_name = false;
        var v_price = false;
        var v_description = false;
        var v_logo = false;

        var el_n = $('#name');
        if (el_n.val().length > 30) {
            v_name = true;
            $('.good-name').after('<span class="text-error">Название товара должно быть меньше 30 символов</span>');
        }
        if (el_n.val().length == 0) {
            v_name = true;
            console.log('aaaaa');
            $('.good-name').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_p = $('#price');
        if (el_p.val().length > 5) {
            v_price = true;
            $('.good-price').after('<span class="text-error">Слишком большое число</span>');
        }
        if (el_p.val().length == 0) {
            v_price = true;
            $('.good-price').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        var el_d = $('#description');
        if (el_d.val().length == 0) {
            v_description = true;
            $('.good-description').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        if ($('form input[type=file]').val().length == 0) {
            v_logo = true;
            $('.good-logo').after('<span class="text-error">Выберите файл</span>');
        }

        return (v_name || v_price || v_description || v_logo);
    }

    $('.add_good').on('submit', function (event) {
        if (validateForm()) {
            event.preventDefault();
        }
    });

    $('.btn-close').click(function () {
        $('#name').val('');
        $('.text-error').remove();
    });


    /*Ajax отправка формы*/
    $('.form_comment').on('submit', function (event) {
        event.preventDefault();
        var text = $('#id_text').val();
        var good_id = parseInt($('.good_id').text());

        $.ajax({
            url: '/write_comment/' + good_id,
            type: 'POST',
            dataType: 'json',
            data: {
                'text': text,
                'csrfmiddlewaretoken': $('.form_comment input[name=csrfmiddlewaretoken]').val()
            },
            error: function () {
                console.log('Error!!!!!!!!!!!')
            },
            success: function (data) {
                $('.users').append('<p class="list_users">' + data.message + '</p>');
                $('#id_text').val('');
            }
        });
    });

    /*Бесконечная прокрутка*/
    var last_good_id = 10;
    $(window).scroll(function () {
        var windowScroll = $(window).scrollTop();
        var windowHeight = $(window).height();
        var documentHeight = $(document).height();

        console.log(windowScroll + ' ' + windowHeight + ' ' + documentHeight);

        if ((windowScroll + windowHeight) >= (documentHeight - 0.2)) {
            $.ajax({
                url: '/add_content',
                type: 'POST',
                dataType: 'json',
                data: {
                    'last_good_id': last_good_id,
                    'csrfmiddlewaretoken': $('.add_good input[name=csrfmiddlewaretoken]').val()
                },
                error: function () {
                    console.log('Error!!!!!!!!!!!')
                },
                success: function (data) {
                    if (data.message != 'stop') {
                        $('.goods_list').append(
                            '<h4>' +
                            '<img class="logo" src="' + data.message.good_logo + '">' +
                            '<a href="/good/' + data.message.good_id + '">' + data.message.good_name + '</' + 'a>' +
                            '</h4>' +
                            '<p>' + data.message.good_description + '</p><hr>'
                        );
                        last_good_id += 1;
                    }
                }
            });
        }
    });
});
