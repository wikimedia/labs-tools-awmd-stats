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
		m = (_m > 9 ? _m : '0' + _m),
		_d = e.date.getDate(),
		d = (_d > 9 ? _d : '0' + _d),
		month = y + '-' + m;

		window.open(baseUrl + "month/" + month, "_self")
	});

	$('#refresh-btn').refreshMe({
		started:function(ele){ele.html("")}
	});
});

/* Refreshing animations */
$.fn.refreshMe = function(opts){
	var $this = this,
	defaults = {
		ms:1500,
		parentSelector:'.panel',
		started:function(){},
		completed:function(){}
	},
	settings = $.extend(defaults, opts);

	var par = this.parents(settings.parentSelector);

	var ms = settings.ms;
	var started = settings.started;		//function before timeout
	var completed = settings.completed;	//function after timeout

	$this.click(function(){
		$this.addClass("fa-spin");
		panelToRefresh.show();
		if (dataToRefresh) {
			started(dataToRefresh);
		}
		setTimeout(function(){
			if (dataToRefresh) {
				completed(dataToRefresh);
			}
			panelToRefresh.fadeOut(800);
			$this.removeClass("fa-spin");
		},ms);
		return false;
	})//click

}/* end function refreshMe */

function getBaseUrl() {

	// use home url link as baseurl, remove protocol
	var baseUrl = document.getElementById('baseurl').getAttribute('href').replace(/^https?:\/\//,'');

	// add actual protocol to fix Flask bug with protocol inconsistency
	baseUrl = location.protocol + "//" + baseUrl
	return baseUrl;
}
