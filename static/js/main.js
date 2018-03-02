jQuery(document).ready( function($){
	
	// base url
	var getUrl = window.location;
	var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];


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

		window.open(base_url + "/month/"+month,"_self")
	});

	// progress bar while loading stats
	var month = $('input#month').val();

	jQuery( "#html_content" ).load( base_url + "/raw/" + month, function( response, status, xhr ) {
		if ( status == "error" ) {
			console.log( xhr.status + " " + xhr.statusText );
		}
	});
});
