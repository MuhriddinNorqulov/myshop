let img = document.querySelector('#product-img'),
    price = document.querySelector('#product-price'),
    name = document.querySelector('#product-name'),
    form = document.querySelector('#quick-form')

let detailBtns = document.querySelectorAll('.product-detail-eye')

for (let item of detailBtns) {
    item.addEventListener('click',  function() {
        let product = JSON.parse(item.dataset.product)
        img.src = product['img']

        price.innerHTML = `$${product['price']}`
        name.innerHTML = product['name']
        form.dataset.product = `${product['id']}`


    })
}


// Product
let products = document.querySelectorAll('.item')

for (let product of products) {
    let product_info = JSON.parse(product.dataset.product)
    let price = product.querySelector('.cart-price')
    if (product_info['stock']) {
        price.innerHTML = `<p class="cart-price-stock"><del>$ ${product_info['price']}</del>$ ${product_info['price']}</p>`
    }

}




