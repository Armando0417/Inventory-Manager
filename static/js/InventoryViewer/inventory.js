/*
    This is the JavaScript code for the products.html page

    Functions:
        highlightText(element, query): Highlights the search query in the element
        handleInput(event): Handles input event for search box
*/


 // Function to highlight text
 function highlightText(element, query) {
    const innerHTML = element.innerHTML;
    const index = innerHTML.toLowerCase().indexOf(query.toLowerCase());
    if (index >= 0) {
        element.innerHTML = innerHTML.substring(0, index) +
            "<span class='highlight'>" + innerHTML.substring(index, index + query.length) + "</span>" +
            innerHTML.substring(index + query.length);
    }
}


function colorByCategory() {
    const categoryColors = {
        'Clothes': '#f77373',
        'Shoes': 'rgb(255, 145, 19)',
        'Accessories': 'rgb(180, 200, 108)',
        'Stationery': '#e575f3',
        'Notebooks': 'rgb(99, 99, 255)',
        'Cups': '#c8af60',
        'Mugs': 'purple',
        'Stickers': 'rgb(255, 199, 94)',
        'Instruments': '#54dbbc',
        'Gifts': '#d4af37'
        // Add any remaining categories here following the same format:
        // "Category name" : "#color_hex_code"

    };

    const items = document.querySelectorAll(".grid-item");

    items.forEach((item) => {
        const category = item.getAttribute('data-category');
        const color = categoryColors[category] || '#fff'; // Use default color if category not found
        item.style.backgroundColor = color;
    });
}

colorByCategory();


function getColorForCategory(category) {
    const categoryColors = {
        'Clothes': '#f77373',
        'Shoes': 'rgb(255, 145, 19)',
        'Accessories': 'rgb(180, 200, 108)',
        'Stationery': '#e575f3',
        'Notebooks': 'rgb(99, 99, 255)',
        'Cups': '#c8af60',
        'Mugs': 'purple',
        'Stickers': 'rgb(255, 199, 94)',
        'Instruments': '#54dbbc',
        'Gifts': '#d4af37'
        // Add any remaining categories here following the same format:
        // "Category name" : "#color_hex_code"

    };

    return categoryColors[category] || '#fff'; // Default color
}

// // Example usage
// document.querySelectorAll('.grid-item').forEach(item => {
//     item.addEventListener('click', () => {
//         const category = item.getAttribute('data-category');
//         // openModal(category);
//     });
// });



// Handle input event for search box
    const searchBox = document.getElementById('search-box');
    searchBox.addEventListener('input', function() {
        const query = searchBox.value.toLowerCase();
        console.log('Search Query:', query); // Debugging log
        const items = document.querySelectorAll('.grid-item');
        items.forEach(item => {
            item.style.display = 'none';
            const name = item.getAttribute('data-name').toLowerCase();
            const id = item.getAttribute('data-id').toLowerCase();
            const price = item.getAttribute('data-price').toLowerCase();
            // const category = item.getAttribute('data-category').toLowerCase();
            const h3 = item.querySelector('h3');

            // Remove previous highlights
            h3.innerHTML = h3.textContent;

            if (name.includes(query) || id.includes(query) || price.includes(query)) {
                item.style.display = 'block';
                highlightText(h3, query);
            }
        });
    });