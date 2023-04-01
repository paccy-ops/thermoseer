$("#myElem").show();
setTimeout(function() { $("#myElem").hide(); }, 10000);

// let previousResponse = null;

// function checkForChanges() {
//   // Send an AJAX request to retrieve the latest data
//   $.ajax({
//     url: "http://127.0.0.1:8000/scanned",
//     method: "GET",
//     success: function (latestResponse) {
//       // Compare the latest response with the previous response
//       if (isEqual(previousResponse, latestResponse)) {
//         // If the latest response is different from the previous response, reload the page
//         $("#contentdisplay").css("background","red");
//         console.log(latestResponse.data.name);
//       }else {
//          $("#contentdisplay").css("display","none");
//       }
//       // Update the previous response to the latest response
//       previousResponse = latestResponse;
//
//     },
//     error: function (xhr, textStatus, errorThrown) {
//       console.log("Error retrieving data from server.");
//     }
//   });
// }
//
// // Deep comparison method using JSON.stringify()
// function isEqual(obj1, obj2) {
//   return JSON.stringify(obj1) === JSON.stringify(obj2);
// }
//
// // Check for changes every 5 seconds
// setInterval(checkForChanges, 2000);





// $(document).ready(function() {
//     $.ajax({
//         url: 'http://127.0.0.1:8000/scanned',
//         type: 'GET',
//         success: function(response) {
//             const data = response.data;
//             const  previousId = data.id
//             console.log(previousId)
//             console.log(response.data.id)
//             const table = $('#my-table tbody');
//             $.each(data, function(i, item) {
//                 const row = $('<tr>');
//                 $('<td>').text(item.id).appendTo(row);
//                 $('<td>').text(item.name).appendTo(row);
//                 row.appendTo(table);
//             });
//         }
//     });
// });

// $.get("http://127.0.0.1:8000/", function(data) {
//   var myData = $("#myData").text(); // Retrieve the data from the HTML element
//   console.log("myData"); // Output the data to the console
// });

// $("#weather").hide();
// setTimeout(function(){ $("#weather").show(); }, 10000);
//
// // setTimeout(function(){
// //    window.location.reload(1);
// // }, 20000);
//
// $('#myElem').one('DOMSubtreeModified', function(){
//     console.log('changed');
// });
//
// console.log("thermoseer")

