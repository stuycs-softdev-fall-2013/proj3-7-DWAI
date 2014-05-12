var http = require('http');
var fs = require('fs');
var url = require('url');


var server = http.createServer(function(req,res){
    var path = url.parse(req.url).pathname;
    var fsCallback = function(err,data){
	if(err) throw err;
	res.writeHead(200);
	res.write(data);
	res.end();
    }
    switch(path){
    case '/hello':
	doc = fs.readFile(__dirname + '/hello.html',fsCallback);
	break;
    default:
	doc = fs.readFile(__dirname + '/index.html',fsCallback);
	break;
    }
}).listen(5000);
console.log('Server running on 127.0.0.1:5000');