document.addEventListener('DOMContentLoaded', function () {
    // Function to open modal and populate data
    function openModal(product) {

        // Open modal
        const modal = document.getElementById('product-modal');
        const modalContent = modal.querySelector('.modal-content');

        // Populate data
        document.getElementById('modal-product-name').innerText = product.name;
        document.getElementById('modal-product-quantity').innerText = `Total Quantity: ${product.quantity}`;
        document.getElementById('modal-product-description').innerText = product.description;
        document.getElementById('modal-product-price').innerText = `Price: $${product.price}`;
        document.getElementById('modal-product-category').innerText = `Category: ${product.category}`;
        
        // Fetch product variations
        fetch(`/product/${product.id}/variations`)
            .then(response => response.json())
            .then(data => {
                const variationsList = document.getElementById('modal-product-variations');
                variationsList.innerHTML = ''; 

                if (data.length === 0) {
                    variationsList.innerText = 'No variations available.';
                }
                else {
                    console.log("Data:", data);
                    
                    data.forEach(variation => {
                        const li = document.createElement('li');
                        li.innerText = `Size: ${variation.size}, Quantity: ${variation.quantity}`;
                        variationsList.appendChild(li);
                    });
                }})
            .catch(error => {
                console.error('Error fetching product variations:', error);
            });

            const borderColor = getColorForCategory(product.category);
            modalContent.style.borderColor = borderColor;
            
            modal.style.display = 'block';
            modalContent.classList.add('active');
            modal.style.color = borderColor;
              
        console.log('Color grabbed', borderColor);
        console.log('Color of the modal', modalContent.style.borderColor);

    }

    // Close modal when close button is clicked
    const closeModalButton = document.querySelector('.close-button');
    if (closeModalButton) {
        closeModalButton.addEventListener('click', function() {
            const modal = document.getElementById('product-modal');
            modal.style.display = 'none';
        });
    }

    // Close modal when clicking outside of the modal content
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('product-modal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Add event listeners to grid items to open the modal
    const gridItems = document.querySelectorAll('.grid-item');
    gridItems.forEach(item => {
        item.addEventListener('click', function() {
            const product = {
                id: item.getAttribute('data-id'),
                name: item.getAttribute('data-name'),
                price: item.getAttribute('data-price'),
                quantity: item.getAttribute('data-quantity'),
                description: item.getAttribute('data-description'),
                category: item.getAttribute('data-category'),
            };
            openModal(product);
        });
    });
});
