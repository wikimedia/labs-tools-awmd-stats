jQuery(document).ready( function($){   
	 $('#datepicker button').datepicker({
		format: "mm-yyyy",
		startView: "months", 
		minViewMode: "months"
	});

	// progress bar while loading stats
	$.ajax({
            method: 'GET',
            url: '/month/',
            dataType: 'json',
            success: function() { },
            error: function() { },
            progress: function(e) {
                //make sure we can compute the length
                console.log(e);
                if(e.lengthComputable) {
                    //calculate the percentage loaded
                    var pct = (e.loaded / e.total) * 100;

                    //log percentage loaded
                    //console.log(pct);
                    $('#progress').html(pct.toPrecision(3) + '%');
                }
                //this usually happens when Content-Length isn't set
                else {
                    console.warn('Content Length not reported!');
                }
            }
        }); 
		
});
