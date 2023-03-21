require("dotenv").config();
// require('./DB/connection');

const express = require("express");
const app = express();
const PORT = process.env.PORT || 3123;
const body_parser = require("body-parser");
const path = require("path");
const { spawn } = require("child_process");
let pythonProcess = spawn('python', ["./Src/check.py"]);


//Helpers
const { getVideos, getHomeVideos } = require("./Helpers/get-videos");


//middlewares used
app.use(express.json());
app.use(body_parser.urlencoded({ extended: false }));
app.use(express.static(path.join(`${__dirname}`, `../Public`)));

//pre-defined things--------------
app.set("view engine", "ejs");
app.set("views", path.join(`${__dirname}`, `../Templates/Views/`));
/* use partial path in using include() */


//routers
app.get("/", async (req, res) => {
    try {

        return res.status(200).render("index");
    } catch (error) {
        return res.status(500).json(error);
    }
});



// Define a route to search for YouTube videos
app.post("/search", async (req, res) => {
    try {
        const query = req.body.query || "MERN STACK PLAYLIST";
        console.log(query);
        let videos = (query) ? await getVideos(query) : await getHomeVideos();
        // console.log(videos);

        pythonProcess.stdin.write(JSON.stringify(videos));
        pythonProcess.stdin.end();

        pythonProcess.stdout.on('data', (data) => {

            let result = JSON.parse(data);
            console.log(result);
            return res.status(200).json(result);
            // return res.status(201).json(videos);
        });

    } catch (error) {
        return res.status(401).send(error);
    }
});




app.listen(PORT, () => { console.log(`server runs on http://127.0.0.1:${PORT}`); });