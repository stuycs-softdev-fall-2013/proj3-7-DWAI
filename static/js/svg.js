var draw = function(){
    var s,namespace,pen;
    var penDown,currPath,cpathid;    
    var oldMidPtX,oldMidPtY,midPtX,midPtY;
    var redoStack,data;
    var layerList,currLay;

    var drawPath = function(d){
	var p = document.createElementNS(namespace,'path');
	p.setAttribute('class','layer' + currLay);
	p.setAttribute('id','path' + cpathid);
	p.setAttribute('d',d);
	p.setAttribute('stroke',pencolor());
	p.setAttribute('fill','transparent');
	p.setAttribute('stroke-width',2*pen.getAttribute('r'));
	p.setAttribute('stroke-linejoin','round');
	p.setAttribute('stroke-linecap','round');
	p.setAttribute('opacity',1);
	if(!layerList[currLayer()])
	    p.style.visibility = 'hidden';
	
	s.append(p);	
    };

    var undo = function(){
	if(cpathid > 0){
	    currPath = $('#path'+(cpathid-1));
	    redoStack.push(currPath);
	    currPath.remove();
	    cpathid--;
	}
    }
    var redo = function(){
	currPath = redoStack.pop();
	if(currPath != null){
	    s.append(currPath);
	    cpathid++;
	}
    }
    var save = function(){
	var imgdata = s.children();
	console.log(imgdata);
	$.post(window.location.href,{imgdata:imgdata});
	return imgdata;
    }
    var load = function(img){
	s = $('#svg');
	s.text('Your browser does not support the SVG tag');
	
	namespace = "http://www.w3.org/2000/svg"
	pen = document.createElementNS(namespace,"circle");
	pen.setAttribute('id','pen');
	pen.setAttribute('cx',0);
	pen.setAttribute('cy',0);
	pen.setAttribute('r',30);
	pen.setAttribute('stroke','#000000');
	pen.setAttribute('fill','#FFFFFF');
	s.append(pen);
	if(img)
	    s.innerHTML=s.innerHTML + img;
	penDown = false;
	
	cpathid = document.getElementsByTagName("path").length;
	layerList = [true];
	redoStack = [];
	currLay = layerList.length - 1;

	s.mousemove(function(e){
	    pen.setAttribute('cx',e.offsetX);
	    pen.setAttribute('cy',e.offsetY);
	    if(penDown){
		currPath = $('#path' + cpathid);
		midPtX = e.offsetX;
		midPtY = e.offsetY;
		var pdata = currPath.attr('d');
		currPath.attr('d',pdata + ' Q ' + (oldMidPtX + e.offsetX>>1) + ' ' + (oldMidPtY + e.offsetY>>1) + ' ' + midPtX + ' ' + midPtY + ' ');
		oldMidPtX = midPtX;
		oldMidPtY = midPtY;
	    }
	});
	s.mousedown(function(e){
	    penDown = true;
	    oldMidPtX = e.offsetX;
	    oldMidPtY = e.offsetY;
	    cpath = 'M ' + oldMidPtX + ' ' + oldMidPtY + ' ';
	    drawPath(cpath);
	});
	s.mouseup(function(e){
	    penDown = false;
	    cpathid++;
	});	
    }
    var newLayer = function(){
	layerList.push(true);
	currLay++;
    }
    var currLayer = function(){
	return currLay;
    }
    var hideLayer = function(){
	var strokesInLayer = $('.layer' + currLayer());
	for(var i = 0;i < strokesInLayer.length;i++)
	    strokesInLayer[i].style.visibility='hidden';
	layerList[currLayer()] = false;
    }
    var showLayer = function(){
	var strokesInLayer = $('.layer' + currLayer());
	for(var i = 0;i < strokesInLayer.length;i++)
	    strokesInLayer[i].style.visibility='visible';
	layerList[currLayer()] = true;
    }
    var changeLayer = function(newLayer){
	currLay = newLayer - 1;
    }
    var pencolor = function(){
	return '#000000';
    }
    return {
	undo: undo,
	redo: redo,
	save: save,
	load: load,
	newLayer: newLayer,
	currLayer: currLayer,
	hideLayer: hideLayer,
	showLayer: showLayer,
	changeLayer: changeLayer
    };
}();
draw.load();
