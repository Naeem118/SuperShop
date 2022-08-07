const productCardsContainer = document.querySelector("[product-cards-container]")
const productCardTemplate = document.querySelector("[product-card-template]")

let products = []
var cnt = 0

if(!window.location.href.includes('products')){
    fetch("/productsdata/")
    .then(response => response.json())
    .then(data => {
        products = data.data.map(product => {
            const card = productCardTemplate.content.cloneNode(true).children[0]
            const carouselSlide = card.querySelector("[carousel-slide]")
            const cardBody = card.querySelector("[card-body]")
            const title = card.querySelector("[product-name]")
            const priceRange = card.querySelector("[price-range]")
            const stock = card.querySelector("[product-stock]")
            const rating = card.querySelector("[product-rating]")
            const offer = card.querySelector("[product-offer]")
            const cart = card.querySelector("[product-cart]")

            /** Taking the image template of a single card */
            const cardImageContainer = card.querySelector("[card-image-container]")
            const imageTemplate = card.querySelector("[product-image-template]")
            /** Carousel indecator of the corresponding image */
            const carouselIndicatorContainer = card.querySelector("[indicators-container]")
            const carouselIndicatorTemplate = card.querySelector("[indicator-template]")

            carouselSlide.id = "carousel" + product.PRODUCT_ID

            title.textContent = product.PRODUCT_NAME
            stock.textContent = 'In Stock: ' + product.STOCK_QUANTITY
            if(product.PRODUCT_RATING == 0){
                rating.textContent = 'Rating: n/a'
            }else{
                rating.textContent = 'Rating: ' + product.PRODUCT_RATING
            }
            offer.textContent = product.OFFER_PCT + '% OFF'

            let unit=''
            if(product.UNIT_ID==1){
                unit='kg'
            }
            else if(product.UNIT_ID==2){
                unit='pc'
            }
            else if(product.UNIT_ID==3){
                unit='litre'
            }

            priceRange.textContent = 'Tk . ' + product.PRODUCT_PRICE + ' / ' + product.FOR_UNIT + " " + unit

            /** Iterate throgh all the images of a product */
            fetch("/productPhotosPath/" + product.PRODUCT_ID)
            .then(responsePath => responsePath.json())
            .then(values => {
                let active = true
                let count = 0
                values.paths.forEach(path => {
                    const imageDiv = imageTemplate.content.cloneNode(true).children[0]
                    const image = imageDiv.querySelector("[product-image]")
                    const button = carouselIndicatorTemplate.content.cloneNode(true).children[0]
                    image.src = path.PATH
                    if(active) {
                        image.parentElement.classList.add('active')
                        button.classList.add('active')
                        button.setAttribute("aria-current", "true")
                        active = false
                    }
                    button.setAttribute("data-bs-target", "#carousel" + product.PRODUCT_ID)
                    button.setAttribute("data-bs-slide-to", "" + count)
                    count += 1
                    button.setAttribute("aria-label", "Slide " + count)
                    carouselIndicatorContainer.append(button)
                    cardImageContainer.append(imageDiv)
                })
            })
            card.querySelectorAll("[data-bs-target]").forEach(element => {
                element.setAttribute("data-bs-target", "#carousel" + product.PRODUCT_ID)
            })
            cardBody.onclick = function() {
                //console.log("Clicked")
                location.href = "/product-detail/" + product.PRODUCT_ID
            }
            if(window.location.href.includes('searchstore')){
                cart.removeAttribute("hidden"); 
                const productCardsItemCount = document.querySelector("[item-count]");
                const categoryId = document.getElementById('categoryid');
                console.log(categoryId.value)
                console.log(product.CATEGORY_ID)
                if ((product.STOCK_QUANTITY!=0 && product.CATEGORY_ID==categoryId.value)){
                    cnt = cnt + 1;
                }
                else{
                    card.setAttribute("hidden", true);
                }
                if(cnt==0 || cnt==1){
                    productCardsItemCount.textContent = cnt + " item found"
                }
                else{
                    productCardsItemCount.textContent = cnt + " items found"
                }
            }
            else if(window.location.href.includes('store')){
                cart.removeAttribute("hidden"); 
                const productCardsItemCount = document.querySelector("[item-count]");
                const productName = document.getElementById('productname').value.trim()
                if ((product.STOCK_QUANTITY!=0 && productName=="") || 
                    (product.STOCK_QUANTITY!=0 && product.PRODUCT_NAME.toLowerCase().includes(productName.toLowerCase()))){
                    cnt = cnt + 1;
                }
                else{
                    card.setAttribute("hidden", true);
                }
                if(cnt==0 || cnt==1){
                    productCardsItemCount.textContent = cnt + " item found"
                }
                else{
                    productCardsItemCount.textContent = cnt + " items found"
                }
            }
            //cart.setAttribute("href","{% url 'product-detail' "+ product.PRODUCT_ID + "%}")
            cart.onclick = function() {
                location.href = "/product-detail/" + product.PRODUCT_ID
            }

            productCardsContainer.append(card)
            if(product.STOCK_QUANTITY == 0){
                card.setAttribute("hidden", true)
            }
            return {
                    element: card
                }
        })

        $('.carousel').carousel({
            interval: false,
        });
    })
} 
