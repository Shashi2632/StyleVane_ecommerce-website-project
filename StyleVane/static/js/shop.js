
$(document).ready(function () {
    $('.add-to-cart').click(function (event) {
        event.preventDefault(); // Prevent the default link click behavior

        // Get the product ID from the data attribute
        var productId = $(this).data('product-id');

        // Send an AJAX request to add the product to the cart
        $.ajax({
            type: 'GET',
            url: '/add_to_cart/' + productId, // Modify the URL to match your Django view
            success: function (response) {
                // Handle the response (e.g., show a success message)
                alert('Product added to cart!');
            },
            error: function (error) {
                // Handle any errors that occur during the AJAX request
                alert('Error adding product to cart.');
            }
        });
    });
});

