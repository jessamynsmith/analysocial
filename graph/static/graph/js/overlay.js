$(document).ready(function() {
    $('#id_sync_posts').on('click', function() {
        new Overlay('<div class="loader-container"><div class="loader"></div><div class="loading">Loading...</div></div>',
            {classes: ['bg-black-transparent']});
    });
});
