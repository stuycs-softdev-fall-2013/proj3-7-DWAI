var canvasScript = function(){
    var canvas = document.getElementById("cvs");
    var ctx=canvas.getContext("2d");

    var pen = function(e){
	ctx.clearRect(0,0,canvas.width,canvas.height);
	ctx.beginPath();
	ctx.setLineDash([1,1]);
	ctx.arc(e.x-10,
		e.y-10,
		10,0,2*Math.PI);//x,y,radius,startAng,endAng
	ctx.stroke();
    }


    var getMousePos = function(canvas,e){
	var rect = canvas.getBoundingClientRect();
	return {
	    x: e.clientX - rect.left,
	    y: e.clientY - rect.top
	};
    }
    canvas.addEventListener('mousemove',function(e){
	var mousePos = getMousePos(canvas,e);
	pen(e);
    });
}();

