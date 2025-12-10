const express = require('express');
const cors = require('cors');
const app = express ();
app.use(cors());
app.use(express.json());
const PORT = 8081;
app.listen(PORT, () => {console.log("Sever Listening on PORT:", PORT)});

app.get("/add", (req, res) => {
    var1 = parseFloat(req.query.a);
    var2 = parseFloat(req.query.b);

    if(isNaN(var1) || isNaN(var2)){
        res.status(400);
        res.send("Error: 400 Bad Reqeest (params)");
        return;
    }

    result = var1 + var2;

    res.send("" + result);
});

app.get("/sub", (req, res) => {
    var1 = parseFloat(req.query.a);
    var2 = parseFloat(req.query.b);

    if(isNaN(var1) || isNaN(var2)){
        res.status(400);
        res.send("Error: 400 Bad Reqeest (params)");
        return;
    }

    result = var1 - var2;

    res.send("" + result);
});
app.get("/mul", (req, res) => {
    var1 = parseFloat(req.query.a);
    var2 = parseFloat(req.query.b);

    if(isNaN(var1) || isNaN(var2)){
        res.status(400);
        res.send("Error: 400 Bad Reqeest (params)");
        return;
    }

    result = var1 * var2;

    res.send("" + result);
});
app.get("/div", (req, res) => {
    var1 = parseFloat(req.query.a);
    var2 = parseFloat(req.query.b);

    if(isNaN(var1) || isNaN(var2)){
        res.status(400);
        res.send("Error: 400 Bad Reqeest (params)");
        return;
    }
    if (var2 == 0){
        res.status(400);
        res.send("Error: 400 Bad Reqeest (Div 0)");
        return;
    }

    result = var1 / var2;

    res.send("" + result);
});