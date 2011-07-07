// What is $(document).ready ? See: http://flowplayer.org/tools/using.html#document_ready
/*global jQuery:false, document: false, window: false, setTimeout:false*/
jQuery(function ($) {

    var resizeCarousel, carousels, ap, api;

    resizeCarousel = function (carousel, scrollable, elems) {
        var base_height, scrollable_height, outer_height, $carousel;

        // Adjust height of the carousel to the max height of the elements.
        base_height = Math.max.apply(null,
            $(elems).map(function () {
                return $(this).height();
            }).get()
        );
        if (base_height < $(carousel).height()) {
            base_height = $(carousel).height() - $('.navi').outerHeight(true);
        }
        $(elems).height(base_height);

        // Re-size .scrollable. Since all .tileItem lements have equal height
        // by now, we can rely on the first element in the set.
        scrollable_height = $(elems).eq(0).outerHeight(true);
        $(scrollable).height(scrollable_height);

        // Re-size .carousel.
        outer_height = $(scrollable).outerHeight(true) + $('.navi').outerHeight(true);
        $carousel = $(carousel);
        if ($carousel.height() < outer_height) {
            // 'resized.carousel' is a custom trigger that 3rd-party code can use for
            // binding events to the moment when a carousel is resized. 'carousel' namespace
            // minimizes chances of conflicting with any other custom trigger of the same 'resized'
            // name.
            // In your custom JS code to bind an event to the moment when a carousel has been
            // completely loaded and resized use something like this:
            // $("#my-special-case .carousel").bind('resized.carousel', function (event, newheight) {
            //     your custom handler for resized.carousel' event
            // });
            // This is helpful if you need to have more than 1 carousel in the same row
            // and want all of them to be the same height - then you bind risizing function to this
            // 'resized.carousel' trigger.
            $carousel.height(outer_height).trigger('resized.carousel', [outer_height]);
        }
    };

    $('.toolBar').hide();
    carousels = $('.carousel');

    carousels.each(function (i) {
        var carousel = this,
            scrollable = $(this).find('.scrollable').eq(0),
            elems = $(scrollable).find('.tileItem'),
            // Set width of all carousel items so they wrap and have correct widths
            scrollable_width = $(scrollable).width();

        for (i = 0; i < elems.length; i += 1) {
            $(elems[i]).css({width: scrollable_width });
        }

        // Use setTimeout here to give other code a chance to bind events.
        // setTimeout 0 causes code to run right after the jQuery load event has finished.
        // setTimeout(function () { resizeCarousel(carousel, scrollable, elems); }, 0);
        setTimeout(function () {
            resizeCarousel(carousel, scrollable, elems);
        }, 0);

        $(scrollable).find('img').load(function (event) {
            // If an image is loaded later we need to resize the whole carousel to fit it
            resizeCarousel(carousel, scrollable, elems);
        });
    });

    // doesn't make sense to enable autoscrolling if more than one
    // carousel is on a page - this just distracts and annoys
    ap = (carousels.length === 1) ? true : false;

    // initialize scrollable
    api = $('div.scrollable').scrollable({
        size: 1,
        clickable: false,
        loop: true
    }).circular().autoscroll({autoplay: ap, steps: 1, interval: 25000}).navigator({api: true});

    // Show toolBar when hovering over a carousel
    $('.carousel').hover(
        function () {
            $(this).find('.toolBar').eq(0).slideToggle('fast').show();
        },
        function () {
            $(this).find('.toolBar').eq(0).slideToggle('fast').hide();
        }
    );
});
