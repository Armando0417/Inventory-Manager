document.addEventListener('DOMContentLoaded', function () {
    // Fetch and display products
    fetch('/products', {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Fetched Data:', data); // Debugging log
        const productList = document.getElementById('product-grid');
        productList.innerHTML = '';
        data.forEach(product => {
            const div = document.createElement('div');
            div.classList.add('grid-item');
            div.setAttribute('data-id', product.id);
            div.setAttribute('data-name', product.name);
            div.setAttribute('data-price', product.price);
            div.setAttribute('data-quantity', product.quantity);
            div.setAttribute('data-category', product.category);

            // Assign class based on category
            switch (product.category.toLowerCase()) {
                case 'clothes':
                    div.classList.add('clothes-border');
                    break;
                case 'notebooks':
                    div.classList.add('notebooks-border');
                    break;
                case 'shoes':
                    div.classList.add('shoes-border');
                    break;
                case 'cups':
                    div.classList.add('cups-border');
                    break;
                case 'mugs':
                    div.classList.add('mugs-border');
                    break;
                case 'stickers':
                    div.classList.add('stickers-border');
                    break;
                default:
                    // Add a default class or handle unexpected categories
                    break;
            }

            div.innerHTML = `<h3>${product.name}</h3><p>Quantity: ${product.quantity}</p><p>Price: $${product.price.toFixed(2)}</p>`;
            productList.appendChild(div);

            // Add click event to open modal (if modal functionality is required)
            div.addEventListener('click', function() {
                try {
                    openModal(product);
                }
                catch (error) {
                    console.error('Error opening modal:', error);
                }

            });
        });
    })
    .catch(error => {
        console.error('Error fetching products:', error);
    });



    // Add product form handling (if adding new products via form)
    const addProductForm = document.getElementById('add-product-form');
    if (addProductForm) {
        addProductForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(addProductForm);
            const data = {
                name: formData.get('name'),
                quantity: formData.get('quantity'),
                price: formData.get('price'),
                category: formData.get('category')
            };

            fetch('/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(product => {
                const productList = document.getElementById('product-grid');
                const div = document.createElement('div');
                div.classList.add('grid-item');
                div.setAttribute('data-id', product.id);
                div.setAttribute('data-name', product.name);
                div.setAttribute('data-price', product.price);
                div.setAttribute('data-quantity', product.quantity);
                div.setAttribute('data-category', product.category);

                // Assign class based on category
                switch (product.category.toLowerCase()) {
                    case 'clothes':
                        div.classList.add('clothes-border');
                        break;
                    case 'notebooks':
                        div.classList.add('notebooks-border');
                        break;
                    case 'shoes':
                        div.classList.add('shoes-border');
                        break;
                    case 'cups':
                        div.classList.add('cups-border');
                        break;
                    case 'mugs':
                        div.classList.add('mugs-border');
                        break;
                    case 'stickers':
                        div.classList.add('stickers-border');
                        break;
                    default:
                        // Add a default class or handle unexpected categories
                        break;
                }

                div.innerHTML = `<h3>${product.name}</h3><p>Quantity: ${product.quantity}</p><p>Price: $${product.price.toFixed(2)}</p>`;
                productList.appendChild(div);

                // Add click event to open modal (if modal functionality is required)
                div.addEventListener('click', function() {
                    // openModal(product);
                });
            })
            .catch(error => {
                console.error('Error adding product:', error);
            });
        });
    }


    

    // Handle view products button (if exists in the context)
    const viewProductsBtn = document.getElementById('view-products-btn');
    if (viewProductsBtn) {
        viewProductsBtn.addEventListener('click', function() {
            window.location.href = '/products';
        });
    }
});
