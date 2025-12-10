const http = require('node:http');
const fs = require('node:fs'); // file system access
const hostname = '0.0.0.0';
const port = 80;

// host 1: www.yggdrasil.local
// host 2: download-ram.yggdrasil.local

const pagehtml = fs.readFileSync('index.html');

const server = http.createServer(
	(req, res) =>
	{ 
		//res.statusCode = 200;
	    //res.setHeader('Content-Type', 'text/plain');
	    //res.end('Hello World\n');

			res.statusCode = 200;
			res.setHeader('Content-Type', 'text/html');
			res.end(pagehtml);
			return;
	}
);


server.listen(port, hostname, () =>
	{
		console.log(`Server running at http://${hostname}:${port}/`);
	}
);
