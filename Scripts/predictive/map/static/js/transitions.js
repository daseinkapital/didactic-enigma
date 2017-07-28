    var $main = $( '#pt-main' ),
		$pages = $main.children( 'div.pt-page' ),
		$iterate = $( '#Page-Transition' ),
		pagesCount = $pages.length,
		current = 0,
		isAnimating = false,  
		endCurrPage = false,
		endNextPage = false,
		animEndEventNames = {
			'WebkitAnimation' : 'webkitAnimationEnd',
			'OAnimation' : 'oAnimationEnd',
			'msAnimation' : 'MSAnimationEnd',
			'animation' : 'animationend'
		},
		// animation end event name
		animEndEventName = animEndEventNames[ Modernizr.prefixed( 'animation' ) ],
		// support css animations
		support = Modernizr.cssanimations;
		
		 $pages.each( function() {
			var $page = $( this );
			$page.data( 'originalClassList', $page.attr( 'class' ) );
		} );

		$pages.eq( current ).addClass( 'pt-page-current' );
    
    
    function onEndAnimation( $outpage, $inpage ) {
		endCurrPage = false;
		endNextPage = false;
		resetPage( $outpage, $inpage );
		isAnimating = false;
	}

	function resetPage( $outpage, $inpage ) {
		$outpage.attr( 'class', $outpage.data( 'originalClassList' ) );
		$inpage.attr( 'class', $inpage.data( 'originalClassList' ) + ' pt-page-current' );
    }

// -------------------------------------------------------------------------------------- // 
//                         MOVE CUBE ROTATE
// -------------------------------------------------------------------------------------- // 
 function gotoPage2(pagenumber) {
     
     if(current == pagenumber) {return true;}
     else {

		if( isAnimating ) {
			return false;
		}

		isAnimating = true;

		var $currPage = $pages.eq( current );

        if( current  != pagenumber ) {
			current = pagenumber;
		}

		var $prevPage = $pages.eq( current ).addClass( 'pt-page-current' ),
			outClass = 'pt-page-rotateSlideOutRight', inClass = 'pt-page-rotateSlideInRight';


		$currPage.addClass( outClass ).on( animEndEventName, function() {
			$currPage.off( animEndEventName );
			endCurrPage = true;
			if( endNextPage ) {
				onEndAnimation( $currPage, $prevPage );
			}
		} );

		$prevPage.addClass( inClass ).on( animEndEventName, function() {
			$prevPage.off( animEndEventName );
			endNextPage = true;
			if( endCurrPage ) {
				onEndAnimation( $currPage, $prevPage );
			}
		} );

		if( !support ) {
			onEndAnimation( $currPage, $prevPage );
		}
     }

	}

// -------------------------------------------------------------------------------------- // 
//                         MOVE CUBE ROTATE
// -------------------------------------------------------------------------------------- // 
 function gotoPage1(pagenumber) {
     
     if(current == pagenumber) {return true;}
     else {

		if( isAnimating ) {
			return false;
		}

		isAnimating = true;

		var $currPage = $pages.eq( current );

        if( current  != pagenumber ) {
			current = pagenumber;
		}

		var $prevPage = $pages.eq( current ).addClass( 'pt-page-current' ),
			outClass = 'pt-page-rotateSlideOutLeft', inClass = 'pt-page-rotateSlideInLeft';


		$currPage.addClass( outClass ).on( animEndEventName, function() {
			$currPage.off( animEndEventName );
			endCurrPage = true;
			if( endNextPage ) {
				onEndAnimation( $currPage, $prevPage );
			}
		} );

		$prevPage.addClass( inClass ).on( animEndEventName, function() {
			$prevPage.off( animEndEventName );
			endNextPage = true;
			if( endCurrPage ) {
				onEndAnimation( $currPage, $prevPage );
			}
		} );

		if( !support ) {
			onEndAnimation( $currPage, $prevPage );
		}
     }

	}