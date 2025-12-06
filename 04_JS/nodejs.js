const http = require('node:http');
const fs = require('node:fs'); // file system access
const hostname = '0.0.0.0';
const port = 80;

// host 1: www.yggdrasil.local
// host 2: download-ram.yggdrasil.local

const page1html = fs.readFileSync('simple-page.html');
const page2html = fs.readFileSync('download-ram.html');

const server = http.createServer(
	(req, res) =>
	{ 
		//res.statusCode = 200;
	    //res.setHeader('Content-Type', 'text/plain');
	    //res.end('Hello World\n');

		if (!req.headers.host) {
			res.statusCode = 400;
			res.end('Error: You bongus forgot the host header!! :(');
			return;
    	}

		const hostname = req.headers.host.split(':')[0]; // remove port numbers cuz doesnt matter
    	if (hostname === 'www.yggdrasil.local') {
			res.statusCode = 200;
			res.setHeader('Content-Type', 'text/html');
			res.end(page1html);
			return;
		} 
		else if (hostname === 'download-ram.yggdrasil.local') {
			res.statusCode = 200;
			res.setHeader('Content-Type', 'text/html');
			res.end(page2html);
			return;
		} else {
			res.statusCode = 404;
			res.end('Unknown website: ' + hostname);
			return;
	    }
	}
);


server.listen(port, hostname, () =>
	{
		console.log(`Server running at http://${hostname}:${port}/`);
	}
);