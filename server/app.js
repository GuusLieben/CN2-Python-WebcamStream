const NodeMediaServer = require('node-media-server');
const express = require('express');
const app = express();

const config = {
  rtmp: {
    port: 1935,
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60
  },
  http: {
    port: 8000,
    allow_origin: '*'
  }
};
 
var nms = new NodeMediaServer(config)
nms.run();

app.use(express.static('viewer'))
app.listen(8080, () => console.log('Started Viewer host!'))