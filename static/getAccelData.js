if (window.DeviceMotionEvent != undefined) {
	window.ondevicemotion = function(e) {
		document.getElementById("val").value = e.accelerationIncludingGravity.y;
	}
}
else {
	document.getElementById("val").value = 0;
}
