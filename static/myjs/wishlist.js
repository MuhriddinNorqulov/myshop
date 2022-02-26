let heartBtns = document.querySelectorAll('.wishlist-update')

for (let item of heartBtns) {
    item.addEventListener('click', function () {
        let product_id = this.dataset.product
        let action = this.dataset.action
        updateCart(product_id, action)
    })
}



function updateCart(product_id, action) {
    var url = action === 'add'? '/wishlist/add/':'/wishlist/remove/'

     fetch(url, {

            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },

            body: JSON.stringify({'product_id': product_id})
        })

            .then(response => {
                return response.json()
            })

            .then(data => {
                console.log('Data:',data)
                if (action === 'remove') {
                    location.reload()
                }
                // location.reload()
            })
}