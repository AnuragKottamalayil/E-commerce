// incrementing cart items amount
$(function(){
    $('.plus').click(function(){
        console.log('working')
        pr_id = $(this).data('id');
        data = {'pr_id':pr_id,'val':1}
        $.get('plus_minus/',data,function(res){
            if(res['success'] == 1){
                cart_qty = res['cart_qty']
                cart_price = res['cart_price']
                total = res['total']
                total_items = res['total_items']
                grand_total = res['grand_total']
                // $('#' + pr_id + ' td').eq(1).html(cart_price);
                // $('#' + pr_id + ' td').eq(2).html(cart_qty);
                $('#quantity' + pr_id).val(cart_qty);
                // $('#quantity' + pr_id).text(cart_qty);
                $('#price' + pr_id).text("₹ " + cart_price);
                $('#total_price').html("₹ " + total);
                $('.total_items').html(total_items);
                $('#grand_total').html("₹ " + grand_total);
                
                

            }
            else{
                cuteAlert({
                    type: "info",
                    title: "Info",
                    message: "You added maximum limit of items",
                    img: "img/info.svg",
                    buttonText: "Okay"
                  })
            }
        })

    })
})
// removing product from cart
$(function(){
    $('.remove').click(function(){
        pr_id = $(this).data('id');
        data = {'pr_id':pr_id};
        $.get('remove/',data,function(res){
            if(res['status'] == true){
                total = res['total']
                total_items = res['total_items']
                grand_total = res['grand_total']
                $('#' + pr_id).remove();
                $('#total_price').html("₹ " + total);
                $('.total_items').html(total_items);
                $('#grand_total').html("₹ " + grand_total);
                
            }
            else{
                total = res['msg']
                cuteAlert({
                    type: "error",
                    title: "Error",
                    message: msg,
                    img: "img/error.svg",
                    buttonText: "Okay"
                  })
            }
        })
    })

})

$(function(){
    $('.minus').click(function(){
        pr_id = $(this).data('id');
        data = {'pr_id':pr_id,'val':2};
        $.get('plus_minus/',data,function(res){
            if(res['cart_qty'] == 0){
                total = res['total']
                total_items = res['total_items']
                grand_total = res['grand_total']
                $('#' + pr_id).remove();
                $('#total_price').html("₹ " + total);
                $('.total_items').html(total_items);
                $('#grand_total').html("₹ " + grand_total);
                
            }
            else{
                cart_qty = res['cart_qty']
                cart_price = res['cart_price']
                total = res['total']
                total_items = res['total_items']
                grand_total = res['grand_total']
                // $('#' + pr_id + ' td').eq(1).html(cart_price);
                // $('#' + pr_id + ' td').eq(2).html(cart_qty);
                // $('#quantity' + pr_id).text(cart_qty);
                $('#quantity' + pr_id).val(cart_qty);
                $('#price' + pr_id).text("₹ " + cart_price);
                $('#total_price').html("₹ " + total);
                $('.total_items').html(total_items);
                $('#grand_total').html("₹ " + grand_total);
            }
        })
    })

})