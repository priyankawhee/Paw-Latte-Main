// Function to add items to the order summary
function addToOrder(itemName, price) {
    // Create a new list item for the order summary
    var li = document.createElement("li");
    li.textContent = itemName + " - ₹" + price;

    // Append the new item to the order list
    document.getElementById("order-list").appendChild(li);
}

// Function to place the order
function placeOrder() {
    var items = [];
    // Get the list of items from the order summary
    var orderItems = document.querySelectorAll("#order-list li");
    orderItems.forEach(function(item) {
        var itemName = item.textContent.split(" - ")[0];
        var itemPrice = parseInt(item.textContent.split(" - ")[1].substring(1)); // Remove the ₹ symbol
        items.push({item: itemName, price: itemPrice});
    });

    // Send a POST request to the Flask route to place the order
    fetch('/place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({items: items}),
    })
    .then(response => response.text())
    .then(data => {
        alert(data); // Show a success message
        // Clear the order summary after placing the order
        document.getElementById("order-list").innerHTML = "";
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error placing the order. Please try again.');
    });
}
