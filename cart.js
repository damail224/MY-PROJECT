let cart = []; // This will hold the cart items

// Add to Cart Function
function addToCart(itemName, itemPrice) {
    // Check if the item already exists in the cart
    const existingItem = cart.find(item => item.name === itemName);

    if (existingItem) {
        existingItem.quantity += 1;
        existingItem.total = existingItem.quantity * itemPrice;
    } else {
        // If item is new, add it to the cart
        cart.push({
            name: itemName,
            price: itemPrice,
            quantity: 1,
            total: itemPrice
        });
    }
    updateCart();
}

// Remove From Cart Function
function removeFromCart(itemName) {
    cart = cart.filter(item => item.name !== itemName); // Remove the item
    updateCart();
}

// Update Cart Function (Refresh the cart display)
function updateCart() {
    const cartBody = document.getElementById("cart-body");
    cartBody.innerHTML = ""; // Clear the cart display

    let grandTotal = 0;

    // Loop through the cart to display items
    cart.forEach(item => {
        grandTotal += item.total;
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.name}</td>
            <td>Ksh ${item.price}</td>
            <td>${item.quantity}</td>
            <td>Ksh ${item.total}</td>
            <td><button onclick="removeFromCart('${item.name}')">Remove</button></td>
        `;
        cartBody.appendChild(row);
    });

    // Update the grand total
    document.getElementById("grand-total").textContent = 'Grand Total: Ksh ${grandTotal}';
}

// Checkout Function
function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
    } else {
        alert("Thank you for your purchase!");
        cart = []; // Clear the cart
        updateCart();
    }
}