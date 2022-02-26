let product_detail = document.querySelector('#product-detail')
product_info = JSON.parse(product_detail.dataset.product)

let product_price = product_detail.querySelector('.box-price')

if(product_info['stock']) {
    product_price.innerHTML = `<span class="box-price2"><del>$${product_info['price']}</del>$${product_info['price']}</span>`
}

