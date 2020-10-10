const express = require('express');
const bodyParse = require("body-parser")

const app = express();

app.use(bodyParse.json());
app.use(bodyParse.urlencoded({extended: false}));

//No path, so executed for all incoming requests
app.use((req, res, next) => {
    //Allows
    res.setHeader("Access-Control-Allow-Origin","*");
    res.setHeader("Access-Control-Allow-Headers","Origin",
    "X-Requested-Width", "Content-Type", "Accept");
    res.setHeader("Access-Control-Allow-Methods", "Get, POST, PATCH, DELETE, OPTIONS");
    next();
});

app.post("/api/posts", (req, res, next) => {
    const chartSettings = req.body;
    console.log(chartSettings);
    res.status(201).json({
        message: 'Chartsettings added successfully'
    });
});

//if this was a use request, then we would need a "next()" in the previous request
app.get('/api/data',(req, res, next) => {
    chartSettings = {ticker: "SPY", timePeriod: 1};
    //do not need return res.json() because
    //it is the last statement in this block
    //don't need 'next()' because there is no next middleware
    res.status(200).json({
        message: "Fetched succesfully",
        chartSettings: chartSettings
    });
});

module.exports = app;

//status 200: everything is ok
//status 201: new resource was created
