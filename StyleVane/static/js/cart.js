document.addEventListener("DOMContentLoaded", function() {
    // Get all the decrease and increase buttons
    var decreaseButtons = document.querySelectorAll(".decrease-quantity");
    var increaseButtons = document.querySelectorAll(".increase-quantity");

    // Add click event listeners for decreasing quantity
    decreaseButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var cartItemId = button.getAttribute("data-cart-item-id");
            var quantityInput = document.getElementById("quantity_" + cartItemId);
            var currentValue = parseInt(quantityInput.value, 10);

            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
                updateQuantityOnServer(cartItemId, quantityInput.value);
            }
        });
    });

    // Add click event listeners for increasing quantity
    increaseButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var cartItemId = button.getAttribute("data-cart-item-id");
            var quantityInput = document.getElementById("quantity_" + cartItemId);
            var currentValue = parseInt(quantityInput.value, 10);

            quantityInput.value = currentValue + 1;
            updateQuantityOnServer(cartItemId, quantityInput.value);
        });
    });

    // Function to update quantity on the server
    function updateQuantityOnServer(cartItemId, newQuantity) {
        

        // Send an AJAX request to update the quantity on the server
        $.ajax({
            type: "GET",
            url: `/update_quantity/${cartItemId}/`,
            data: {
                value: newQuantity,
               
            },
            success: function(response) {
                // Handle the response (e.g., update the total price)
                // You can also update the cart totals on the client side if needed
            },
            error: function(error) {
                // Handle any errors that occur during the AJAX request
                alert("Error updating quantity.");
            },
        });
    }
});