const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const hostname = '0.0.0.0';
const port = 8080;

const server = http.createServer((req, res) => {
    console.log("Request for:", req.url);

    if (req.url === '/' || req.url === '/index.html') {
        fs.readFile('index.html', (err, data) => {
            if (err) {
                res.writeHead(500);
                res.end('Error loading index.html');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
        });

    } else if (req.url === '/script.js') {
        fs.readFile('script.js', (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Script not found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'application/javascript' });
            res.end(data);
        });

    } else if (req.url === '/style.css') {
        fs.readFile('style.css', (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Style not found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/css' });
            res.end(data);
        });

    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

server.listen(port, hostname, () => {
    console.log(`Frontend Server running at http://${hostname}:${port}/`);
});