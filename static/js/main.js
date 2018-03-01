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
	jQuery.ajax({
            method: 'GET',
            url: '/fetch/',
            dataType: 'json',
            success: function() { 
        	console.log('ajax done');
            },
            error: function(e) { 
            	console.log(e);
            },
            progress: function(e) {
            	console.log('ajax progress');
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
