jQuery( document ).ready( function( $ ) {

	// Declare variables before use
	var c_date, c_month, c_year, baseUrl,
		y, _m, m, _d, d, month, date;

	// Get the base url
	baseUrl = getBaseUrl();

	// New Date() object
	c_date = new Date();
	c_month = c_date.getMonth();
	c_year = c_date.getFullYear();

	$( '#datepicker' ).datepicker( {
		format: 'mm/yyyy',
		startView: 'month',
		minViewMode: 'months',
		startDate: new Date( '2014', '01' ),
		// FIXME: Using c_year without +1 causes a bug
		// when user goes to previous month, the next
		// button disappears.
		endDate: '+1y'
	} ).on( 'changeDate', function( e ) {
		y = e.date.getFullYear(),
		_m = e.date.getMonth() + 1,
		m = ( _m > 9 ? _m : '0' + _m ),
		year_month = y + '-' + m;

		window.open( baseUrl + 'month/' + year_month, '_self' )
	} );

	// Refresh the page with some minor animation
	$( '#refresh-btn' ).refreshMe( {
		started: function( e ) { e.html( '' ) }
	} );

} );

/* Refreshing animations */
$.fn.refreshMe = function( opts ) {
	var $this = this,
	defaults = {
		ms: 1500,
		parentSelector: '.panel',
		started: function(){ },
		completed: function() { }
	},
	settings = $.extend( defaults, opts );

	var par = this.parents( settings.parentSelector );

	var ms = settings.ms;
	var started = settings.started;		//function before timeout
	var completed = settings.completed;	//function after timeout

	$this.click( function() {
		$this.addClass( 'fa-spin' );
		panelToRefresh.show();
		if ( dataToRefresh ) {
			started( dataToRefresh );
		}
		setTimeout( function(){
			if ( dataToRefresh ) {
				completed( dataToRefresh );
			}
			panelToRefresh.fadeOut( 800 );
			$this.removeClass( 'fa-spin' );
		}, ms );
		return false;
	})
} /* end function refreshMe */

function getBaseUrl() {
	// use home url link as baseurl, remove protocol
	var baseUrl = document.getElementById( 'baseurl' ).getAttribute( 'href' ).replace( /^https?:\/\//,'' );

	// add actual protocol to fix Flask bug with protocol inconsistency
	baseUrl = location.protocol + '//' + baseUrl
	return baseUrl;
}
