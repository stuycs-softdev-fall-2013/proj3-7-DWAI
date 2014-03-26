var draw = function(){
    var s = document.getElementById('svg');
    var namespace = "http://www.w3.org/2000/svg"
    var pen = document.createElementNS(namespace,"circle");
    pen.setAttribute('id','pen');
    pen.setAttribute('cx',0);
    pen.setAttribute('cy',0);
    pen.setAttribute('r',20);
    pen.setAttribute('stroke','#000000');
    pen.setAttribute('fill','#FFFFFF');
    s.appendChild(pen);
    var penDown = false;
    var cpath;
    var oldMidPtX,oldMidPtY,midPtX,midPtY;
    var cpathid = 0;

    var drawPath = function(d){
	var p = document.createElementNS(namespace,'path');
	p.setAttribute('id','path' + cpathid);
	p.setAttribute('d',d);
	p.setAttribute('stroke','#000000');
	p.setAttribute('fill','transparent');
	p.setAttribute('stroke-width',20);
	p.setAttribute('stroke-linecap','round');
	s.appendChild(p);	
    };
    var movePen = function(e){
	pen.setAttribute('cx',e.offsetX);
	pen.setAttribute('cy',e.offsetY);
	if(penDown){
	    //s.removeChild('#path'+cpathid);
	    midPtX = e.offsetX;
	    midPtY = e.offsetY;
	    cpath = cpath + 'Q ' + (oldMidPtX + e.offsetX>>1) + ' ' + (oldMidPtY + e.offsetY>>1) + ' ' + midPtX + ' ' + midPtY + ' ';
	    
	    console.log(cpath);
	    oldMidPtX = midPtX;
	    oldMidPtY = midPtY;
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
	drawPath(cpath);
	cpathid++;
    });
}();
