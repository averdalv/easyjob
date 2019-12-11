function add_error(element){
    if($(element).css("display") === "none"){
        $(element).css("display","block")
    }
    $("#basic_settings_form_button").attr("disabled","true");
}
function remove_error(element){
    if($(element).css("display") === "block"){
        $(element).css("display","none")
    }
    $("#basic_settings_form_button").removeAttr("disabled");
}

function make_address(){
        remove_error("#location_error");
        var city = $(".city>button>span").text();
        var address = $(".location").val();
        get_lat_lon(city, address, function (lat, lon) {
            $("input[name='lat']").val(lat);
            $("input[name='lon']").val(lon);
        },function(){
            add_error("#location_error");
        });
}

 var n = 0;
    var available_array = [1,1,1,1,1,1,1,1,1,1];
    function get_next_available(){
        for(var i = 0;i<available_array.length;i++){
            if(available_array[i]===1){
                available_array[i] = 0;
                return i;
            }
        }
        return -1;
    }

	$(document).ready(function () {
		$("#datepicker").datepicker({
			format: 'dd/mm/yyyy'
		});
         $(".location").focusout(make_address);
         $("select[name='city']").change(make_address);

         if($("#education-type").val()!==""){
             $("input[name='educational_institution_name']").attr("required","true");
         }
         $("#add_category_button").click(function(event){
            event.preventDefault();
            var n = get_next_available();
            if (n!==-1){
                $(`div[data-category-number='${n}']`).removeClass("non-visible-category");
                $(`input[name='hidden_${n}']`).val("True");
                $(`input[name='price_${n}']`).attr("required","true");
            }
         });
         $("input[type='hidden']input[value='True']").each(function(index,value){
             var name = value.name;
             var n = name.substring(name.lastIndexOf("_")+1);
             if($(`input[name='is_negotiated_${n}']`).is(":checked")){
                 $(`input[name='price_${n}']`).val("");
                $(`input[name='price_${n}']`).removeAttr("required");
                $(`input[name='price_${n}']`).addClass("input-price-disabled");
                $(`input[name='price_${n}']`).prop("disabled",true);
             }
             else {
                 $(`input[name='price_${n}']`).attr("required",true);
             }
              $(`div[data-category-number='${n}']`).removeClass("non-visible-category");
         });
         $(".remove_category_button").click(function(event){
            event.preventDefault();
            var number = $(event.target).attr("data-category-number");
            var num = parseInt(number,10);
            available_array[num] = 1;
            $(`div[data-category-number='${num}']`).addClass("non-visible-category");
            $(`input[name='hidden_${num}']`).val("False");
            $(`input[name='price_${num}']`).removeAttr("required");
         });
         $(".input-negotiated").change(function (event) {
             var name = $(event.target).attr("name");
                var n = name.substring(name.lastIndexOf("_")+1);
            if($(this).is(":checked")) {
                 $(`input[name='price_${n}']`).val("");
                $(`input[name='price_${n}']`).removeAttr("required");
                $(`input[name='price_${n}']`).addClass("input-price-disabled");
                $(`input[name='price_${n}']`).prop("disabled",true);
            }
            else{
                $(`input[name='price_${n}']`).attr("required",true);
                $(`input[name='price_${n}']`).removeClass("input-price-disabled");
                 $(`input[name='price_${n}']`).prop("disabled",false);
            }
         });

         $("#education-type").change(function(event){
             if($(this).val()===""){
                 $("input[name='educational_institution_name']").val("");
                 $("input[name='educational_institution_name']").removeAttr("required");

             }
             else{
                 $("input[name='educational_institution_name']").attr("required","true");
             }
         });

        $("#settings_menu").toggleClass("active");
    });
