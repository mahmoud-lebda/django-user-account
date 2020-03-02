  $("#id_governorate").change(getCity);
/*
function to return city when gov change value with ajax
*/
    function getCity(){
     var url = $("#register_form").attr("data-cities-url");  // get the url of the `load_cities` view
      var governorateId = $(this).val();  // get the selected country ID from the HTML input
      $.get(url,{'governorate': governorateId}).done(success)
    }
function success(data){
 $("#id_city").html(data);
}


/*
function to return city when gov change value with ajax

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'governorate': governorateId       // add the country id to the GET parameters
        },
        success: success
      });
      */

