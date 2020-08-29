// alert(history.state)
function remove_subcategory() {
    $(`.keyword-remove*[data-type='subcategory']`).change();
}

function add_mark(mark_type, mark_text) {
    $(".filter.keyword-input").data("type", mark_type);
    $(".filter.keyword-input").val(mark_text);
    $(".filter.keyword-input-button").click();
}

function remove_mark_change(type) {
    $(`.keyword-remove*[data-type=${type}]`).change();
}

function remove_mark_click(type) {
    $(`.keyword-remove*[data-type=${type}]`).click();
}

function filter(type, value, mark_text) {
    if (type == "category") {
        remove_subcategory();

        if (value == "all") {
            $("#subcategory-widget").css("display", 'none');
        } else {
            $("#subcategory-widget").css("display", 'block');
        }
    }

    if (value != "all") {
        if (search_dict[type] != null) {
            remove_mark_change(type);
        }
        add_mark(type, mark_text);

    } else {
        remove_mark_click(type);
    }
}

function type_click(type, upd_path, skip_update) {
    var mark_text = $(`option[value=${upd_path}]`).text().trim();

    filter(type, upd_path, mark_text);
    search(type, upd_path, skip_update);
}

var subcategories_data = [];

function search(type, upd_path, skip_update) {
    if (type == "category") {
        search_dict['subcategory'] = null;
        load_subcategories(upd_path, function (data) {
            subcategories_data = [{ "name": "Все подкатегории", "value": "all" }].concat(data);
            insert_subcategories(subcategories_data);
        });
    }

    if (upd_path != "all") {
        search_dict[type] = upd_path;
    } else {
        search_dict[type] = null;
    }
    if (!skip_update) {
        window.history.pushState("gg", "", path + dictToURI(search_dict))
        load_orders(path + "api/orders" + dictToURI(search_dict), insert_orders)
    }
}

function remote_click(value){
    // alert(value)
    if(value == true){
        filter('remote', value, "Удаленно")
        search('remote', value)
    }else{
        filter('remote', "all", "");
        search('remote', "all")
    }
    
}

$(document).on('click', "input[name='customer_type']", function () {
    filter('customer_type', $(this).val(), $(this).parent().find("label").text());
    search('customer_type', $(this).val());
});

$(document).on('click', '.page', function (event) {
    event.preventDefault();
    search('page', $(this).data('page'));
    $('html, body').animate({ scrollTop: 0 }, 500);
})

var slider_init_state = null;

$(document).on("click", ".keyword-remove", function () {
    var type = $(this).data('type');

    if (type == "price") {
        search('low_price', 'all', true);
        search('high_price', 'all');
        $(".slider").replaceWith(slider_init_state.clone());
        return;
    }

    if (type == "category") {
        remove_subcategory();
        $("#subcategory-widget").css("display", 'none');
    }

    if (type == "remote"){
        $("#is-remote").prop("checked", false);
    }

    if (type == "customer_type"){
        // alert($("input[id='radio-1'][value='all']").click())
        
    }

    search(type, 'all');

    $(`.${type}`).val('default');
    $(`.${type}`).selectpicker("refresh");

    if (type == "subcategory") {
        insert_subcategories(subcategories_data);
    }
});

$(document).on("click", "#first-order", function () {
    window.location.replace(first_order_path);
});

function filter_slider_add_mark(low, high) {
    remove_mark_change('price');
    add_mark("price", 'Возн. ' + low + '-' + high)
}

function filter_slider_apply() {
    var low = $(".min-slider-handle").attr("aria-valuenow");
    var high = $(".max-slider-handle").attr("aria-valuenow");
    search('low_price', low, true);
    search('high_price', high);
    filter_slider_add_mark(low, high);
}

var filter_slider_id = null;

$(document).ready(function () {
    var params_uri = window.location.href.split("?")[1];
    if(params_uri){
        var params = params_uri.split("&");
        for(var ind in params){
            var key  = params[ind].split("=")[0];
            var value =  params[ind].split("=")[1];
            search_dict[key] = value;
            add_mark(key, value)
        }
    }

    slider_init_state = $(".slider").clone(true, true);
    load_orders(path + "api/orders" + dictToURI(search_dict), insert_orders)
    $("#filter-slider").on("change", function () {
        window.clearTimeout(filter_slider_id);
        filter_slider_id = window.setTimeout(filter_slider_apply, 1000);
    });
});