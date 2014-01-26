var canvasScript = function(){
    var canvas, stage;
    var drawingCanvas;
    var oldPt, oldMidPt;
    var color;
    var stroke;
    var penCursor;
    var isPenDown;
    var currentPath;
    var strokes;
    var redoStack;

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
	penWidth = 10;
	isPenDown = false;
	strokes=[];
	redoStack = [];

	oldPt = new createjs.Point(stage.mouseX, stage.mouseY);
	oldMidPt = new createjs.Point(stage.mouseX, stage.mouseY);


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
	    drawingCanvas.graphics.clear().setStrokeStyle(penWidth, 'round', 'round').beginStroke(color).moveTo(midPt.x, midPt.y).curveTo(oldPt.x, oldPt.y, oldMidPt.x, oldMidPt.y);
	    currentPath.push(midPt);
	}

        oldPt.x = stage.mouseX;
        oldPt.y = stage.mouseY;
	
        oldMidPt.x = midPt.x;
        oldMidPt.y = midPt.y;


        stage.update();
    }

    var handleMouseUp = function() {
	isPenDown = false;
	strokes.push({
	    pensize: penWidth,
	    color: color,
	    path: currentPath
	});
    }
    var handleMouseDown = function() {
	currentPath = [];
	redoStack = [];
	isPenDown = true;
	oldPt = new createjs.Point(stage.mouseX, stage.mouseY);
	oldMidPt = oldPt;
    }
    var drawPath = function(strokeToDraw){
	drawingCanvas.graphics.clear().setStrokeStyle(strokeToDraw.pensize, 'round', 'round').beginStroke(strokeToDraw.color);
	var path = strokeToDraw.path;
	for(var i = 1;i < strokeToDraw.path.length;i++){
	    drawingCanvas.graphics.moveTo(path[i].x,path[i].y).curveTo(path[i].x,path[i].y,path[i-1].x,path[i-1].y);
	    stage.update();
	}
    }
    var redrawAll = function(strokes){
	stage.clear();
	for(var i = 0;i < strokes.length;i++){
	    drawPath(strokes[i]);
	}
	stage.update();
    }
    var undo = function(){
	undostroke = strokes.pop();
	redrawAll(strokes);
	redoStack.push(undostroke);
    }
    var redo = function(){
	var redostroke = redoStack.pop();
	if(redostroke){
	    strokes.push(redostroke);
	    redrawAll(strokes);
	}
    }
    var save = function(){
	var jsonstuff = {
	    "strokes" : strokes
	};
	return jsonstuff;
    }
    
    
    return{
	init:init,
	handleMouseDown:handleMouseDown,
	handleMouseUp:handleMouseUp,
	undo:undo,
	redo:redo
    }
}();

canvasScript.init();
document.getElementById('undo').addEventListener("click",canvasScript.undo);
document.getElementById('redo').addEventListener("click",canvasScript.redo);
//$('.save').addEventListener("click,canvasScript.save);
