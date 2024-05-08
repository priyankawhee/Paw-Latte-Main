// Function to add item to order summary
function addToOrder(itemName) {
    var orderList = document.getElementById('order-list');
    var listItem = document.createElement('li');
    listItem.textContent = itemName;
    // Create remove button
    var removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.onclick = function() {
        removeFromOrder(itemName);
    };
    listItem.appendChild(removeButton);
    orderList.appendChild(listItem);
}

// Function to remove item from order summary
function removeFromOrder(itemName) {
    console.log("Removing item:", itemName); // Add this line to check if the function is being called
    var orderList = document.getElementById('order-list');
    var items = orderList.getElementsByTagName('li');
    for (var i = 0; i < items.length; i++) {
        if (items[i].textContent.trim() === itemName) {
            console.log("Found item to remove:", itemName); // Add this line to check if the correct item is being found
            orderList.removeChild(items[i]);
            break;
        }
    }
}


// Function to place the order
function placeOrder() {
    // Retrieve the selected items
    var selectedItems = [];
    var orderList = document.getElementById('order-list').getElementsByTagName('li');
    for (var i = 0; i < orderList.length; i++) {
        selectedItems.push(orderList[i].textContent.trim());
    }

    // Make a POST request to the server to place the order
    fetch('/place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedItems: selectedItems })
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        if (data.message) {
            // Order placed successfully
            console.log(data.message);
            // Clear the order summary after placing the order
            document.getElementById('order-list').innerHTML = '';
        } else if (data.error) {
            // Error placing order
            console.error(data.error);
            // Optionally, you can show an error message to the user
        }
    })
    .catch(error => {
        // Handle any errors that occur during the request
        console.error('Error placing order:', error);
        // Optionally, you can show an error message to the user
    });
}
