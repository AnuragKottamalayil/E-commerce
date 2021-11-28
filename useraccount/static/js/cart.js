// incrementing cart items amount
$(function(){
    $('.plus').click(function(){
        pr_id = $(this).data('id');
        data = {'pr_id':pr_id,'val':1}
        $.get('plus_minus/',data,function(res){
            if(res['success'] == 1){
                cart_qty = res['cart_qty']
                cart_price = res['cart_price']
                total = res['total']
                $('#' + pr_id + ' td').eq(1).html(cart_price);
                $('#' + pr_id + ' td').eq(2).html(cart_qty);
                $('#total_price').html('Total = ' + total);

            }
            else{
                alert('No more available')
            }
        })

    })
})
// removing cart items
$(function(){
    $('.minus').click(function(){
        pr_id = $(this).data('id');
        data = {'pr_id':pr_id,'val':2};
        $.get('plus_minus/',data,function(res){
            if(res['cart_qty'] == 0){
                $('#' + pr_id).remove();
            }
            else{
                cart_qty = res['cart_qty']
                cart_price = res['cart_price']
                total = res['total']
                $('#' + pr_id + ' td').eq(1).html(cart_price);
                $('#' + pr_id + ' td').eq(2).html(cart_qty);
                $('#total_price').html('Total = ' + total);
            }
        })
    })

})