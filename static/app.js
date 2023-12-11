$(document).ready(function(){
    // Variable to hold the timeout ID
    let closeDropdownTimeout;

    // Handle dropdown open on mouseover
    $(document).on('mouseover', '.dropdown-toggle', function() {
        var $dropdown = $(this).closest('.dropdown');
        $dropdown.addClass('show');
        $dropdown.find('.dropdown-menu').addClass('show');

        // Clear any existing timeout to prevent closing
        clearTimeout(closeDropdownTimeout);
    });

    // Handle dropdown open on click
    $(document).on('click', '.dropdown-toggle', function() {
        let $dropdown = $(this).closest('.dropdown');
        $dropdown.toggleClass('show');
        $dropdown.find('.dropdown-menu').toggleClass('show');
    });

    // Handle closing the dropdown with a delay
    $('.dropdown').on('mouseout', function(event){
        let $dropdown = $(this);
        closeDropdownTimeout = setTimeout(function() {
            if (!$(event.relatedTarget).closest('.dropdown').length) {
                $dropdown.removeClass('show');
                $dropdown.find('.dropdown-menu').removeClass('show');
            }
        }, 300); // 500 milliseconds delay
    });

    // Cancel the timeout if the user re-enters the dropdown area
    $('.dropdown').on('mouseover', function() {
        clearTimeout(closeDropdownTimeout);
    });
});

// Toggle button from outline to solid when clicked to add to favriote
document.getElementById('toggleButton').addEventListener('click', function() {
    var button = this;
    if (button.classList.contains('btn-outline-success')) {
        button.classList.remove('btn-outline-success');
        button.classList.add('btn-success');
    } else {
        button.classList.remove('btn-success');
        button.classList.add('btn-outline-success');
    }
});