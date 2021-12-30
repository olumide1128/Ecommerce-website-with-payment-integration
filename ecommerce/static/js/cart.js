
var updateBtns = document.getElementsByClassName("update-cart");

for(var i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);
    
        console.log('USER:', user);
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action);
        }else{
            updateUserOrder(productId, action);
        }

      
    })
}


var removeBtns = document.getElementsByClassName("remove-item");

for(var i=0; i < removeBtns.length; i++){
    removeBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        console.log('productId:', productId);
    
        console.log('USER:', user);
        if(user === 'AnonymousUser'){
            removeCookieItem(productId);
        }else{
            removeUserOrderItem(productId);
        }

      
    })
}


function addCookieItem(productId, action){
    console.log("Not logged in...");

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1 
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }

    console.log("Cart:", cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload();

}


function updateUserOrder(productId, action){
    console.log('User is logged in, seding data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data);
        location.reload()
    })
}


function removeUserOrderItem(productId){
    console.log('User is logged in, seding data...');

    var url = '/remove_item/';

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId':productId})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data);

        items = data['items'];
        total = data['total'];

        var elem = document.getElementById(productId);
        elem.parentNode.removeChild(elem);

        document.getElementById("no_items").innerHTML = items;
        document.getElementById("total").innerHTML = '$'+total;
        //location.reload()
    })
}


function removeCookieItem(productId){
    
    delete cart[productId];  

    console.log("Cart:", cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload();
}