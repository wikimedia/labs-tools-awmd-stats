jQuery(document).ready( function($){   
	 $('#datepicker button').datepicker({
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

		window.open("/month/"+month,"_self")
	});

	// progress bar while loading stats
	$( "#html_content" ).load( "/raw/", function( response, status, xhr ) {
	  if ( status == "error" ) {
		var msg = "Sorry but there was an error: ";
		$( "#error" ).html( msg + xhr.status + " " + xhr.statusText );
	  }
	});

		
});
