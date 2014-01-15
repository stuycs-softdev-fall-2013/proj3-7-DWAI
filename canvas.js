var canvasScript = function(){
    var canvas, stage;
    var drawingCanvas;
    var oldPt, oldMidPt;
    var color;
    var stroke;
    var penCursor;
    var isPenDown;

    var init = function(){
	if (window.top != window) {
            document.getElementById("header").style.display = "none";
	}
	canvas = document.getElementById("cvs");
	
	//check to see if we are running in a browser with touch support
	stage = new createjs.Stage(canvas);
	stage.autoClear = false;
	stage.enableDOMEvents(true);
	
	createjs.Touch.enable(stage);
	createjs.Ticker.setFPS(30);
	
	drawingCanvas = new createjs.Shape();
	color = "#FF00FF";
	stroke = 40;
	isPenDown = false;
	penCursor = new createjs.Shape();
	penCursor.graphics.beginStroke("gray").drawCircle(stroke/2,stroke/2,stroke/2);
	penCursor.cache(0,0,stroke,stroke);
	oldPt = new createjs.Point(stage.mouseX, stage.mouseY);


	stage.addEventListener("stagemousedown", handleMouseDown);
	stage.addEventListener("stagemouseup", handleMouseUp);
	stage.addEventListener("stagemousemove" , pen);
	
	stage.addChild(drawingCanvas);
	stage.addChild(penCursor);
	stage.update();
    }


    var pen = function(event) {
	var midPt = new createjs.Point(oldPt.x + stage.mouseX>>1, oldPt.y+stage.mouseY>>1);

	if(isPenDown){
	    drawingCanvas.graphics.clear().setStrokeStyle(stroke, 'round', 'round').beginStroke(color).moveTo(midPt.x, midPt.y).curveTo(oldPt.x, oldPt.y, oldMidPt.x, oldMidPt.y);
	    
	}
	penCursor.setTransform(stage.mouseX-stroke/2,stage.mouseY-stroke/2);
	penCursor.updateCache('use');

        oldPt.x = stage.mouseX;
        oldPt.y = stage.mouseY;
	
        oldMidPt.x = midPt.x;
        oldMidPt.y = midPt.y;


        stage.update();
    }

    var handleMouseUp = function(event) {
	isPenDown = false;
    }
    var handleMouseDown = function(event) {
	isPenDown = true;
	oldPt = new createjs.Point(stage.mouseX, stage.mouseY);
	oldMidPt = oldPt;
    }

    init();
}();
