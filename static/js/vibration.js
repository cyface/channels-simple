<script>
// detect vibration support
navigator.vibrate = navigator.vibrate || navigator.webkitVibrate || navigator.mozVibrate || navigator.msVibrate || null;

if (navigator.vibrate) {

	// enable form
	var node = {}, i, name = "nosupport,params,vibrations,duration,delay,stop".split(",");
	for (i = 0; i < name.length; i++) {
		node[name[i]] = document.getElementById(name[i]);
	}

	// form submit event
	node.params.onsubmit = function(e) {
		e.preventDefault();

		var v = [], i,
			vib = node.vibrations.value || 0,
			dur = node.duration.value || 0,
			del = node.delay.value || 0;

		// define vibration settings
		for (i = 0; i < vib; i++) {
			v = v.concat([dur, del]);
		}

		// do vibration
		navigator.vibrate(v);

	};

	// stop event
	node.stop.onclick = function(e) {
		e.preventDefault();
		navigator.vibrate(0);
	};

	node.nosupport.style.display = "none";
	node.params.style.display = "block";

}
</script>
