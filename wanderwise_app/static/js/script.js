/* // Select the button and the mobile menu
const mobileMenuButton = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu2');

// Add event listener to the button to open the mobile menu
mobileMenuButton.addEventListener('click', function() {
    // Add the 'open' class to show the menu
    mobileMenu2.classList.add('open');

    // Automatically close the menu after 5 seconds
    setTimeout(function() {
        mobileMenu2.classList.remove('open');
    }, 5000); // 5000 milliseconds = 5 seconds
}); */


// FAQ Functionality
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(function(item) {
    item.addEventListener('click', function() {
        // Toggle the visibility of the answer
        const answer = this.querySelector('.faq-answer');
        const isVisible = answer.style.display === 'block';

        // Hide all other FAQ answers
        faqItems.forEach(function(i) {
            const ans = i.querySelector('.faq-answer');
            ans.style.display = 'none';
        });

        // Show the clicked answer if it was not visible before
        if (!isVisible) {
            answer.style.display = 'block';
        }
    });
});