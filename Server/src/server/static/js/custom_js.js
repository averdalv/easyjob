 $(document).ready(
     function(){
         $(".account-type-label-firm").on('click',function(e){
           label_for = $(this).attr('for');
           if(label_for==='firm-radio'){
               $(".changing-input-pp-div>input").prop("required",false);
               $(".changing-input-pp-div").css("display",'none');
                $(".changing-input-firm-div").css("display",'block');
                 $(".changing-input-firm-div>input").prop("required",true);
           }
          else if(label_for==='pp-radio'){
               $(".changing-input-firm-div>input").prop("required",false);
               $(".changing-input-firm-div").css("display",'none');
                $(".changing-input-pp-div").css("display",'block');
                 $(".changing-input-pp-div>input").prop("required",true);
           }
         })
     });