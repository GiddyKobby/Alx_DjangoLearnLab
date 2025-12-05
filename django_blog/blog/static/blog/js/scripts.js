// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');

    // Example interactive feature
    const contentDiv = document.querySelector('.content');
    if (contentDiv) {
        contentDiv.addEventListener('click', () => {
            console.log("Content area clicked!");
        });
    }
});
