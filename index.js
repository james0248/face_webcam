const Express = require("express");
const app = Express();
const server = require("http").createServer(app);
const io = require("socket.io").listen(server);

const spawn = require("child_process").spawn;
const jpeg = require("jpeg-js");
const process = spawn("python", ["Image_Process_prime.py"]);

app.set('port', 3000);

process.stdout.on("data", data => {
    const width = 640;
    const height = 480;
    const frameData = new Buffer(width * height * 4);
    for(let i = 0; i < 480; i++) {
        for(let j = 0; j < 640; j++) {
            frameData[640 * 4 * i + 4 * j] = data[640 * 3 * i + 3 * j];
            frameData[640 * 4 * i + 4 * j + 1] = data[640 * 3 * i + 3 * j + 1];
            frameData[640 * 4 * i + 4 * j + 2] = data[640 * 3 * i + 3 * j + 2];
            frameData[640 * 4 * i + 4 * j + 3] = 0XFF;
        }
    }
    const imageData = {
        data: frameData,
        width: width,
        height: height
    };
    const jpegImageData = jpeg.encode(imageData, 50);
    process.emit("jpeg", jpegImageData.data.toString('base64'));
});

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html")
})

io.on("connection", socket => {
    console.log("io connected!");
    process.on("jpeg", data => socket.emit("data", data));
})

server.listen(app.get('port'));
