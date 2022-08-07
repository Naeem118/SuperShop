$(function () {
    'use strict';
    // Showing page loader
    $(window).on('load', function () {
        setTimeout(function () {
            $(".page_loader").fadeOut("fast");
        }, 200);
   });

    $('.hideMessage').on('click',function(){
        document.getElementById("message").style.display = "None";
    });

    $(".product-magnify-gallery").lightGallery();
});

setTimeout(function(){
    $('#message').fadeOut('slow');
}, 4000);
function onUDClickUser(header, msg, csrf_token, postmsg, urlpage){
    console.log(postmsg)
    Confirm.open({
        title: header,
        message: msg,
        onok: () => {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": csrf_token },
                url: urlpage,
                data: {
                    "YES" : postmsg,
                },
                success: function(data){
                    console.log(data.url)
                    window.location.href=data.url
                },
                dataType: "json"
            });
            return false;
        }
    })
}










// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end