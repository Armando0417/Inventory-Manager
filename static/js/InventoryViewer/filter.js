document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const gridItems = document.querySelectorAll('.grid-item');
    
    if (filterButtons.length > 0) {
        console.log('Filter Buttons:', filterButtons); // Debugging line
    }
    if (gridItems.length > 0) {
        console.log('Grid Items:', gridItems); // Debugging line
    }


    if (filterButtons && gridItems) {
        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = button.getAttribute('data-filter');
                console.log('Filter:', filter); // Debugging line
                gridItems.forEach(item => {
                    if (filter === 'all' || item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
});
