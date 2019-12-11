var url = 'https://nominatim.openstreetmap.org/?format=json&addressdetails=1&q=';
var filter = '&format=json&accept-language=ru&limit=1';

function load_coord(text, callback) {
    text = text.split(' ').join('+');
    $.ajax({
        type: "GET",
        url: url + text + filter,
        dataType: "json",
        success: callback,
        error: function (data) {
            console.log(data)
        }
    })
}

function proccess_lat_lon(data, callback) {
    var lat = (parseFloat(data.boundingbox[0]) + parseFloat(data.boundingbox[1])) / 2;
    var lon = (parseFloat(data.boundingbox[2]) + parseFloat(data.boundingbox[3])) / 2;
    callback(lat, lon)
}

function get_lat_lon(city, address, callback, callback_error) {
    load_coord(city + " " + address, function (data) {
        if (data.length > 0) {
            proccess_lat_lon(data[0], callback)
        } else {
            if (callback_error) {
                callback_error();
            }
            load_coord(city, function (data) {
                proccess_lat_lon(data[0], callback);
            })
        }
    })
}