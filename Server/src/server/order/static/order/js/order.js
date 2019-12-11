function bookmark_click(e) {
    if(e) e.preventDefault();
    $("#bookmark").toggleClass('bookmarked');
}

$(document).ready(function () {

    var bookmark = false;

    $.ajax({
        type: "GET",
        url: bookmark_url,
        dataType: "json",
        data: {
            csrfmiddlewaretoken: csrf,
            order_id: order_id
        },
        success: function (data) {
            bookmark = data.is_bookmarked

            if (bookmark) {
                bookmark_click()
            }
        },
        error: function (data) {
            // console.log(data)
        }
    });

    $('.bookmark-icon').on('click', bookmark_click);
    $('.bookmark-button').on('click', bookmark_click);

    $(document).on('click', "#bookmark", function () {
        $.ajax({
            type: "POST",
            url: bookmark_url,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: csrf,
                order_id: order_id
            },
            success: function (data) {
                console.log(data)
            },
            error: function (data) {
                // console.log(data)
            }
        });
    });
});

