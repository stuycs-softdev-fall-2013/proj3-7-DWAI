var draw = function(){
    var s = document.getElementById('svg');
    var namespace = "http://www.w3.org/2000/svg"
    var pen = document.createElementNS(namespace,"circle");
    pen.setAttribute('id','pen');
    pen.setAttribute('cx',0);
    pen.setAttribute('cy',0);
    pen.setAttribute('r',30);
    pen.setAttribute('stroke','#000000');
    pen.setAttribute('fill','#FFFFFF');
    s.appendChild(pen);
    var penDown = false;
    var currPath;
    var oldMidPtX,oldMidPtY,midPtX,midPtY;
    var cpathid = 0;
    var redoStack = [];
    var data;
    var drawPath = function(d){
	var p = document.createElementNS(namespace,'path');
	p.setAttribute('id','path' + cpathid);
	p.setAttribute('d',d);
	p.setAttribute('stroke','#000000');
	p.setAttribute('fill','transparent');
	p.setAttribute('stroke-width',2*pen.getAttribute('r'));
	p.setAttribute('stroke-linecap','round');
	s.appendChild(p);	
    };
    var movePen = function(e){
	pen.setAttribute('cx',e.offsetX);
	pen.setAttribute('cy',e.offsetY);
	if(penDown){
	    currPath = document.getElementById('path' + cpathid);
	    midPtX = e.offsetX;
	    midPtY = e.offsetY;
	    currPath.setAttribute('d',currPath.getAttribute('d') + ' Q ' + (oldMidPtX + e.offsetX>>1) + ' ' + (oldMidPtY + e.offsetY>>1) + ' ' + midPtX + ' ' + midPtY + ' ');
	    
	    oldMidPtX = midPtX;
	    oldMidPtY = midPtY;
	}
    }
    var undo = function(){
	if(cpathid > 0){
	    currPath = document.getElementById('path'+(cpathid-1));
	    redoStack.push(currPath);
	    s.removeChild(currPath);
	    cpathid--;
	}
    }
    var redo = function(){
	currPath = redoStack.pop();
	if(currPath != null){
	    s.appendChild(currPath);
	    cpathid++;
	}
    }
    s.addEventListener('mousemove',movePen);
    s.addEventListener('mousedown',function(e){
	penDown = true;
	oldMidPtX = e.offsetX;
	oldMidPtY = e.offsetY;
	cpath = 'M ' + oldMidPtX + ' ' + oldMidPtY + ' ';
	drawPath(cpath);
    });
    s.addEventListener('mouseup',function(){
	penDown = false;
	cpathid++;
    });
    var save = function(){
	return s.innerHTML;
    }
    return {
	undo: undo,
	redo: redo,
	save: save
    };
}();
