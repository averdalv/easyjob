function insert_subcategories(response) {
    var subcategories = $("select.subcategory");
    var ul = $(".subcategory>div>ul")

    subcategories.html("");
    ul.html("");

    if (response.length == 0){
        $("#subcategories-main-div").css("display", 'none');
    }else{
        $("#subcategories-main-div").css("display", 'block');
    }

    response.forEach(function (subcategory, index) {
        subcategories.append(
            `<option class="bs-title-option" value="${subcategory.value}" ${index == 0 ? "selected" : ""}>
                ${subcategory.name}
            </option>`
        )
        ul.append(`
                <li data-original-index="${index}" class="${index == 0 ? " selected" : ""}">
                    <a tabindex="0" class="" data-tokens="null" role="option"
                    aria-disabled="false" aria-selected="false">
                    <span class="text">${subcategory.name}</span>
                    <span class="glyphicon glyphicon-ok check-mark"></span>
                    </a>
                </li>`
        )

        if (index == 0) {
            $(".subcategory>button>.filter-option").text(subcategory.name);
        }
    });
}

function load_subcategories(category_value, callback) {
    $.ajax({
        type: "GET",
        url: "/order/api/subs/",
        data: {
            csrfmiddlewaretoken: csrf,
            category: category_value
        },
        success: callback,
    });
}

function dictToURI(dict) {
    var str = [];
    for (var p in dict) {
        if (dict[p]) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
        }
    }
    return str.length > 0 ? "?" + str.join("&") : str;
}

function create_paginator(response) {
    $(".paginator").html("");
    if (response.has_other_pages) {
        var st = `
        <div class="pagination-container margin-top-30 margin-bottom-60">
            <nav class="pagination">
                <ul>`;

        var en = `
                </ul>
            </nav>
        </div>`;

        var previous = "";
        var body = "";
        var next = "";

        if (response.has_previous) {
            previous = `
            <li class="pagination-arrow">
                <a data-page="${response.previous_page_number}" href="#" class="page ripple-effect">
                    <i class="icon-material-outline-keyboard-arrow-left"></i>
                </a>
            </li>
            `;
        }

        for (var cur = 1; cur <= response.page_range; ++cur) {
            if (cur == response.number) {
                body += `<li><a href="#" data-page="${cur}" class="page current-page ripple-effect">${cur}</a></li>`;
            } else {
                body += `<li><a href="#" data-page="${cur}" class="page ripple-effect">${cur}</a></li>`;
            }
        }

        if (response.has_next) {
            next = `
            <li class="pagination-arrow">
                <a data-page="${response.next_page_number}" href="#" class="page ripple-effect">
                    <i class="icon-material-outline-keyboard-arrow-right"></i>
                </a>
            </li>
            `;
        }

        $(".paginator").html(st + previous + body + next + en);
    }
}

function insert_orders(response) {
    orders = response['orders'];
    create_paginator(response);
    var orders_div = $("#orders");
    orders_div.html("");

    if (orders.length == 0) {
        orders_div.append(`
            <div class="container">
                <div class="row">
                    <div class="col-xl-12">
                        <section id="not-found" class="center margin-top-50 margin-bottom-25">
                            <h2><i class="icon-line-awesome-hand-peace-o"></i></h2>
                            <p>В данной категории нет активных заданий ;( </p>
                        </section>
                        <div class="row">
                            <div class="col-xl-8 offset-xl-2">
                                <div class="intro-banner-search-form not-found-search margin-bottom-50">
                                    <div class="intro-search-field ">
								        <input id="intro-keywords" type="text" disabled placeholder="Будь первым!">
							        </div>
                                    <div class="intro-search-button">
                                        <button id="first-order" class="button ripple-effect">Создать</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `);
    }

    for (var ind in orders) {
        var order = orders[ind];
        orders_div.append(
            `<a href="${order_url_base + "/" + order.id}" class="task-listing">
            <div class="task-listing-details">
                <div class="task-listing-description">
                    <h3 class="job-listing-title">
                        ${order.name}
                        ${
            order.is_my ?
                '<span class="dashboard-status-button green">Ваш заказ</span>' :
                ''
            }
                    </h3>

                    <ul class="task-icons">
                        <!-- <li><i class="icon-material-outline-location-on"></i> San Francisco</li> 
                        <li><i class="icon-material-outline-access-time"></i> ${order.time_created}</li>
                        <li><i class="icon-material-outline-access-time"></i> ${order.time_end}</li> -->
                    </ul>
                    <p class="task-listing-text">${order.description}</p>
                    <div class="task-tags">
                        <span>${order.category.name}</span>
                        ${order.subcategory ? "<span>" + order.subcategory.name + "</span>" : ""}        
                    </div>
                </div>
            </div>

            <div class="task-listing-bid">
                <div class="task-listing-bid-inner">
                    <div>
                        <span style="vertical-align: top"
                            class="dashboard-status-button ${order.status_style}">
                            ${order.status.name}
                        </span>
                    </div>
                    <div class="task-offers dashboard-status-button grey">
                        <h4 style="padding: 4px">
                            ${
            order.is_fixed_price ?
                order.price_high + " грн" :
                order.price_low + " - " + order.price_high + " грн"
            }
                        </h4>
                        <!-- <span>Fixed Price</span> -->
                    </div>
                    ${
            order.is_respond ?
                '<span class="button">Вы откликнулись</span>' :
                ''
            }
                </div>
            </div>
        </a>`);
    }
}

function load_orders(url, callback) {
    $.ajax({
        type: "GET",
        url: url,
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: callback
    });
}