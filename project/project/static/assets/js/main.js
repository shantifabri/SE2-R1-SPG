$(function() {
   
   $.ajax({
      url: "/getdate",
      type: 'GET',
      dataType: 'json', // added data type
      success: function(res) {
         var k=res.date.split(" ")[0];
         var [d,m,y] =k.split("-");
          
         var result = new Date(y+"-"+m+"-"+d);
         result.setDate(result.getDate() + 7);
         var datestring = ("0" + result.getDate()).slice(-2) + "-" + ("0"+(result.getMonth()+1)).slice(-2) + "-" + result.getFullYear()

         $('#pick-date').pickadate({
            format: 'dd-mm-yyyy',
            formatSubmit: 'dd-mm-yyyy',
            min: k,
            max: datestring,
            disable: [
               1, 2, 3, 7
             ]
         });
      }
   });   

});