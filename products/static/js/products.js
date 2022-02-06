
  $(function(){
    $(document).on("click", ".butn", function(){
      console.log('success')
      val = $(this).data('id');
      data = {'val':val}
      $.get('add_to_cart/',data,function(res){
        if(res['success'] == 1){
          cuteAlert({
            type: "success",
            title: "Success",
            message: "Product added to cart successfully",
            img: "img/success.svg",
            buttonText: "Continue shopping"
          })
        }
        else if(res['success'] == 2){
          cuteAlert({
            type: "success",
            title: "Success",
            message: "Product added to cart successfully",
            img: "img/success.svg",
            buttonText: "Continue shopping"
          })
        }
        else if(res['success'] == 0){
          cuteAlert({
            type: "info",
            title: "Info",
            message: "No more products available",
            img: "img/info.svg",
            buttonText: "Okay"
          })
        }
        else if(res['success'] == 3){
          console.log('Please login')
          cuteAlert({
            type: "warning",
            title: "Login",
            message: "Please login to add items to cart",
            img: "img/warning.svg",
            buttonText: "Okay"
          })
        }
      })
    })
  })

$(function(){
  $('.brand').click(function(){
    val = $(this).data('id');
    data = {'brand':val}
    $.get('product_by_brand/',data,function(res){
      $('#product div').empty();
      $('.main div').empty();
      pr_count = res['pr_count'];
      var newDiv = "";
      var i ;
      for(i=0; i<pr_count; i++){
        // console.log(res['pr_obj'][i].fields.pr_price);
        // console.log(res['pr_obj'][i].fields.pr_name);
        // console.log(res['pr_obj'][i].fields.pr_image);
        // console.log(res['pr_obj'][i].fields.pr_quantity);
        // console.log(res['pr_obj'][i].pk);
        var pr_price = res['pr_obj'][i].fields.pr_price;
        var pr_name = res['pr_obj'][i].fields.pr_name;
        var pr_image = res['pr_obj'][i].fields.pr_image;
        var pr_quantity = res['pr_obj'][i].fields.pr_quantity;
        var pr_id = res['pr_obj'][i].pk;

        // newDiv += `
        // <img style="width: 142px;height: 256px;" class="ml-5 mt-4" src="/media/${pr_image}" alt="Card image cap">
        //             <h5>${pr_name} - ₹${pr_price}</h5>
        //             <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
        //             <a href="#" data-id=${pr_id} class="btn btn-danger butn">Add to cart</a>
        //             <a href="/product_details/${pr_id}/" class="btn btn-primary">Details</a>
        //           `

        $('#parent').append(`
                            <div class="col-md-4 p-3 col-sm-2 ">
                            <div class="card text-center mx-auto" style="width: 18rem;">
                            <img style="width: 142px;height: 256px;" class="ml-5 mt-4" src="/media/${pr_image}" alt="Card image cap">
                            <div id='jqueryproducts' class="card-body">
                            <h5>${pr_name} - ₹${pr_price}</h5>
                            <a href="#" data-id=${pr_id} class="btn btn-danger butn">Add to cart</a>
                            <a href="/product_details/${pr_id}/" class="btn btn-primary">Details</a>
                            </div>
                            </div>
                            </div>
                            `)
      }
      
    
      
      
      
      
      
     
    })
    
  })

})


