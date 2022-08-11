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

const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const addProductPic = document.getElementById('addProductPic');
const addProductPicBtn = document.getElementById('addProductPicBtn');
const picLimit = document.getElementById('picLimit');
const addBtnProduct = document.getElementById('addBtnProduct');
const productId = document.getElementById('productid');
const udform = document.getElementById('udform');

// function onUDClickProduct(header, msg, csrf_token, postmsg, urlpage,productid){
//     console.log(postmsg)
//     Confirm.open({
//         title: header,
//         message: msg,
//         onok: () => {
//             $.ajax({
//                 type: "POST",
//                 headers: { "X-CSRFToken": csrf_token },
//                 url: urlpage,
//                 data: {
//                     "YES" : postmsg,
//                     "product_id": productid
//                 },
//                 success: function(data){
//                     console.log(data.url)
//                     window.location.href=data.url
//                 },
//                 dataType: "json"
//             });
//             return false;
//         }
//     })
// }

// function onUDClickUser(header, msg, csrf_token, postmsg, urlpage){
//     console.log(postmsg)
//     Confirm.open({
//         title: header,
//         message: msg,
//         onok: () => {
//             $.ajax({
//                 type: "POST",
//                 headers: { "X-CSRFToken": csrf_token },
//                 url: urlpage,
//                 data: {
//                     "YES" : postmsg,
//                 },
//                 success: function(data){
//                     console.log(data.url)
//                     window.location.href=data.url
//                 },
//                 dataType: "json"
//             });
//             return false;
//         }
//     })
// }

// Profile image upload function start
if(file != null) {
    file.addEventListener('change', function(){
    //this refers to file
        const choosedFile = this.files[0];
        if (choosedFile) {
            const reader = new FileReader(); 
            reader.addEventListener('load', function(){
                img.setAttribute('src', reader.result);
            });
            reader.readAsDataURL(choosedFile);
        }
    });
}

// const Confirm = {
//     open (options) {
//         options = Object.assign({}, {
//             title: '',
//             message: '',
//             okText: 'Continue',
//             cancelText: 'Cancel',
//             onok: function () {},
//             oncancel: function () {}
//         }, options);
        
//         const html = `
//             <div class="confirm">
//                 <div class="confirm__window">
//                     <div class="confirm__titlebar">
//                         <span class="confirm__title">${options.title}</span>
//                         <button class="confirm__close">&times;</button>
//                     </div>
//                     <div class="confirm__content">${options.message}</div>
//                     <div class="confirm__buttons">
//                         <button class="confirm__button confirm__button--ok confirm__button--fill">${options.okText}</button>
//                         <button class="confirm__button confirm__button--cancel">${options.cancelText}</button>
//                     </div>
//                 </div>
//             </div>
//         `;

//         const template = document.createElement('template');
//         template.innerHTML = html;

//         // Elements
//         const confirmEl = template.content.querySelector('.confirm');
//         const btnClose = template.content.querySelector('.confirm__close');
//         const btnOk = template.content.querySelector('.confirm__button--ok');
//         const btnCancel = template.content.querySelector('.confirm__button--cancel');

//         confirmEl.addEventListener('click', e => {
//             if (e.target === confirmEl) {
//                 options.oncancel();
//                 this._close(confirmEl);
//                 console.log('Returning false');
//                 //return false;
//             }
//         });

//         btnOk.addEventListener('click', () => {
//             options.onok();
//             this._close(confirmEl);
//             console.log('Returning true');
//             //return true;
//         });

//         [btnCancel, btnClose].forEach(el => {
//             el.addEventListener('click', () => {
//                 options.oncancel();
//                 this._close(confirmEl);
//                 console.log('Returning false');
//                // return false;
//             });
//         });

//         document.body.appendChild(template.content);
//     },

//     _close (confirmEl) {
//         confirmEl.classList.add('confirm--close');

//         confirmEl.addEventListener('animationend', () => {
//             document.body.removeChild(confirmEl);
//         });
//     }
// };

// if(udform!=null){
//     udform.addEventListener('submit', function ( event ) {
//         console.log("paise")
//         event.preventDefault();
//     });
// }

const addNewProductPic = value => {
    if(addProductPicBtn.disabled != true){
        addProductPicBtn.disabled = true;
        let idOfProduct = productId.value 
        const url = `/fetch_no_of_product_pics/${idOfProduct}/`;
        fetch(url, {
            method: "GET"
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            let noOfProduct = data[0]
            if(noOfProduct==5){
                picLimit.style.display="block";
            }
            else{
                //console.log(noOfProduct)
                addBtnProduct.style.display="block";
                var c=1;
                var brk = document.createElement("span");
                brk.innerHTML="<br>";
                addProductPic.appendChild(brk);
                for (var input = noOfProduct+1; input <= 5; input++) {
                    var newProductPicLabel = document.createElement("label");
                    newProductPicLabel.for = "upload"+input;
                    newProductPicLabel.innerHTML="House Pic " + c + ":";
                    newProductPicLabel.style="padding-left: 5%;"
                    addProductPic.appendChild(newProductPicLabel);
                    var newProductPic = document.createElement("input");
                    newProductPic.type="file";
                    newProductPic.accept="image/*";
                    newProductPic.name="upload"+input;
                    newProductPic.style="padding-left: 5%;"
                    addProductPic.appendChild(newProductPic);
                    var brk = document.createElement("span");
                    brk.innerHTML="<br><br>";
                    addProductPic.appendChild(brk);
                    c++;
                }
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
}

try{
    addProductPicBtn.onclick = () => addNewProductPic();
}
catch{
    //console.log("On product detail page!!");
}