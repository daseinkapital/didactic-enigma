(function($) {
    "use strict";

    setTimeout(function(){jQuery('#overlay').fadeOut("slow")},3000);
    
    $('a').click(function(e) {
        e.preventDefault();
        newLocation = this.href;
        $('body').fadeOut("slow", newpage);
    });
    
    function newpage() {
        window.location = newLocation;
    }

})(jQuery);
