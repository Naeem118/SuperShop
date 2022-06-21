const productCardsContainer = document.querySelector("[product-cards-container]")
const productCardTemplate = document.querySelector("[product-card-template]")
 
let products = []
 
if(!window.location.href.includes('yourproducts')){
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
            /** Taking the image template of a single card */
            const cardImageContainer = card.querySelector("[card-image-container]")
            const imageTemplate = card.querySelector("[product-image-template]")
            /** Carousel indecator of the corresponding image */
            const carouselIndicatorContainer = card.querySelector("[indicators-container]")
            const carouselIndicatorTemplate = card.querySelector("[indicator-template]")
 
            carouselSlide.id = "carousel" + product.PRODUCT_ID
 
            title.textContent = product.PRODUCT_NAME
            stock.textContent = 'In Stock: ' + product.STOCK_QUANTITY
            rating.textContent = 'Rating: ' + product.PRODUCT_RATING
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
                console.log("Clicked")
                location.href = "/product-detail/" + product.PRODUCT_ID
            }
            productCardsContainer.append(card)
            return {
                    element: card
                }
        })
 
        $('.carousel').carousel({
            interval: false,
        });
    })
}