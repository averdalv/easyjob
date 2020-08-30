function insert_popular_categories(categories) {
    var popular = $("#popular_categories_sep");
    var categories_content = "";
    categories.forEach(function (category) {
        categories_content += `
        <div class="col-xl-3 col-md-6">
            <a href="/orders/?category=${category[1]}" class="photo-box small"
                data-background-image="${image_base_url + "/" + category[1]+'.jpg'}"
                style="background-image: url(${image_base_url + "/" + category[1]+'.jpg'});">
                <div class="photo-box-content">
                    <h3>${category[0]}</h3>
                    <span>${category[2]}</span>
                </div>
            </a>
        </div>
        `
    });
    $(categories_content).insertAfter(popular);
}

function insert_orders_now(orders) {
    var $orders_now_div = $("#orders_now_div");
    $orders_now_div.html("");
    var len = Math.min(orders.length, 5);
    for (var i = 0; i < len; ++i) {
        var order = orders[i];
        $orders_now_div.append(`
            <a href="${orders_path + order.id}" class="job-listing with-apply-button">
                <div class="job-listing-details">
                    <div class="job-listing-description">
                        <h3 class="job-listing-title">${order['name']}</h3>
                        <div class="job-listing-footer">
                            <ul>
                                <li><i class="icon-material-outline-business"></i> ${order['payment']['name']}
                                    <div class="verified-badge" title="Verified Employer"
                                        data-tippy-placement="top"></div>
                                </li>
                                <li><i class="icon-material-outline-location-on"></i> ${order['location']['city']['name']}</li>
                                <li><i class="icon-material-outline-business-center"></i>${order['category']['name']}</li>
                                <li><i class="icon-material-outline-access-time"></i>${order['time_created']}</li>
                            </ul>
                        </div>
                    </div>
                    <span class="list-apply-button ripple-effect">Смотреть</span>
                </div>
            </a>
        `);
    }
}
function get_word_by_number(number){
    if(number%10 == 1 && number != 11){
        return "Задание";
    }
    else if(number == 2 || number == 3 || number == 4){
        return "Задания";
    }
    return "Заданий";
}
function insert_active_cities(cities) {
    var active = $("#active_cities_sep");
    var cities_content = "";
    cities.forEach(function (city) {
        cities_content += `           
        <div class="col-xl-3 col-md-6">
            <a href="/orders/?city=${city[1]}" class="photo-box"
                data-background-image="${image_base_url + "/" + city[1]+'.jpg'}"
                style="background-image: url(${image_base_url + "/" + city[1]+'.jpg'});">
                <div class="photo-box-content">
                    <h3>${city[0]}</h3>
                    <span>${city[2]} ${get_word_by_number(city[2])}</span>
                </div>
            </a>
        </div>
        `
    });
    $(cities_content).insertAfter(active)
}

function search_main(){
    var category_search = $("#category-search");
    var index = parseInt(category_search.parent().find("div>ul>li.selected").attr("data-original-index")) + 1;
    var category_value = category_search.find(`:nth-child(${index})`).attr("data-value");

    var city_search = $("#city-search");
    var index = parseInt(city_search.parent().find("div>ul>li.selected").attr("data-original-index")) + 1;
    var city_value = city_search.find(`:nth-child(${index})`).attr("data-value");

    // alert(category_value + " " + city_value)

    var uri_dict = {};
    if(category_value != "undefined"){
        uri_dict['category'] = category_value;
    }
    if(city_value != "undefined"){
        uri_dict['city'] = city_value;
    }
    
    window.location.replace(orders_path + dictToURI(uri_dict));
}

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: categories_url,
        dataType: "json",
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: function (data) {
            insert_popular_categories(data);
            // console.log(data)
        },
        error: function (data) {
            // console.log(data)
        }
    });

    load_orders(orders_path + "api/orders", function (response) {
        insert_orders_now(response['orders'])
    });

    $.ajax({
        type: "GET",
        url: cities_url,
        dataType: "json",
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: insert_active_cities,
        error: function (data) {
            // console.log(data)
        }
    });
});