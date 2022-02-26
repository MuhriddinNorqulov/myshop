let updateBtns = document.querySelectorAll('.update-cart')

for (let form of updateBtns) {
    form.addEventListener('submit', function (event) {
        event.preventDefault()
        let product_id = this.dataset.product
        let action = this.dataset.action
        let update = action === 'update'? true: false


        try {
            var count = this.querySelector('.product-count').value
        }
        catch(err) {
            var count = '1'
        }

        update_cart(product_id,'update', count, update)

    })
}


// Remove from Cart

let removeBtns = document.querySelectorAll('.product-remove')
for (let item of removeBtns) {
    item.addEventListener('click', function () {
        let product_id = this.dataset.product
        update_cart(product_id, 'remove')


    })
}



function update_cart(product_id, action, count='1', isupdate=false){
    let url = null;

    if (action === 'remove') {
        url = '/cart/remove/'
    } else if (action === 'update') {
        url = '/cart/add/'
    }

    console.log(url)
    fetch(url, {

            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },

            body: JSON.stringify({'product_id': product_id,'count': count, 'isupdate': isupdate})
        })

            .then(response => {
                return response.json()
            })

            .then(data => {
                if (action === 'remove') {
                    location.reload()
                }

                let quantity_tag = document.querySelector('#cart-qunatity')
                let cart = JSON.parse(data)

                let qunatity = cart['quantity']

                quantity_tag.innerHTML = `${qunatity}`

                try {
                    let item_price_tag = document.querySelector(`#item-price${product_id}`),
                        total_price_tag = document.querySelector('#total-price'),
                        quantity_tag2 = document.querySelector('#cart-qunatity2')

                    let item_price = cart['item-price'],
                        total_price = cart['total-price']

                    item_price_tag.innerHTML = `<p>$ ${item_price}</p>`
                    total_price_tag.textContent = `$ ${total_price}`
                    quantity_tag2.textContent = `${qunatity}`
                }
                catch (err) {
                    console.log(err)
                }



            })
}