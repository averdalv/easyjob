function set_price_from_slider() {
    var low = $(".min-slider-handle").attr("aria-valuenow");
    var high = $(".max-slider-handle").attr("aria-valuenow");
    $('input[name="price_low"]').val(low);
    $('input[name="price_high"]').val(high);
}

$(document).ready(function () {
    $("select.categories").on('change', function (a) {
        var category_value = $("select.categories option:selected").attr("value");
        load_subcategories(category_value, insert_subcategories);
    })

    $(".perform-type-label").on('click', function (e) {
        label_for = $(this).attr('for');
        if (label_for === 'customer') {
            $(".changing-input-city").css("display", 'block');
            $(".changing-input-address").css("display", 'block');
        }
        else if (label_for === 'performer') {
            $(".changing-input-city").css("display", 'block');
            $(".changing-input-address").css("display", 'none');
        }
        else if (label_for === 'remote') {
            $(".changing-input-city").css("display", 'none');
            $(".changing-input-address").css("display", 'none');
        }
    })

    $(".payment-type-label").on('click', function (e) {
        label_for = $(this).attr('for');
        if (label_for === 'after') {
            $(".after-payment-type").css("display", 'block');
        }
        else if (label_for === 'before') {
            $(".after-payment-type").css("display", 'none');
        }
    })

    $(".slider").click(function () {
        $(".tooltip.tooltip-main.top").css("display", 'block');
        $(".slider-selection").css("display", 'block');
        $(".price>input").val("");
        $('input[name="is_fixed_price"]').val("False");
    })

    $(".price>input").keyup(function () {
        var cur_val = $(this).val();
        if (cur_val != "") {
            $(".tooltip.tooltip-main.top").css("display", 'none');
            $(".slider-selection").css("display", 'none');
            $('input[name="is_fixed_price"]').val("True");
            $('input[name="price_high"]').val(cur_val);
        } else {
            $(".tooltip.tooltip-main.top").css("display", 'block');
            $(".slider-selection").css("display", 'block');
            $('input[name="is_fixed_price"]').val("False");
        }
    })

    $(".slider").on("change", set_price_from_slider);

    $(".location").focusout(function () {
        var city = $(".city>button>span").text();
        var address = $(".location").val();

        get_lat_lon(city, address, function (lat, lon) {
            $("#lat").val(lat)
            $("#lon").val(lon)
        });
    });

    $("#datetimepicker-start").datetimepicker({
        format: 'm/d/Y H:i'
    });

    $("#datetimepicker-end").datetimepicker({
        format: 'm/d/Y H:i'
    });

    // Init price if nothing selected
    set_price_from_slider();
});

$("#orders_menu").toggleClass("active");