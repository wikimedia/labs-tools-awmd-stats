jQuery(document).ready( function($){
	
	// base url
	baseUrl = getBaseUrl();


	$('#datepicker').datepicker({
		format: "mm-yyyy",
		startView: "months", 
		minViewMode: "months"
	}).on('changeDate', function(e) {
		var y = e.date.getFullYear(),
		_m = e.date.getMonth() + 1,
		m = (_m > 9 ? _m : '0'+_m),
		_d = e.date.getDate(),
		d = (_d > 9 ? _d : '0'+_d),
		month = y + '-' + m;

		window.open(baseUrl + "month/"+month,"_self")
	});

	// progress bar while loading stats
	var month = $('input#month').val();

	jQuery( "#html_content" ).load( baseUrl + "raw/" + month, function( response, status, xhr ) {
		if ( status == "error" ) {
			console.log( xhr.status + " " + xhr.statusText );
		}
	});

	/* Refresh page when refresh icon is clicked */
	$('#refresh-btn').click(function() {
		location.reload();
	});
});

function getBaseUrl() {

	// use home url link as baseurl, remove protocole
	var baseUrl = document.getElementById('baseurl').getAttribute('href').replace(/^https?:\/\//,'');

	// add actual protocol to fix Flask bug with protocol inconsistency
	baseUrl = location.protocol + "//" + baseUrl 
	return baseUrl;
}