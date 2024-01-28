const express = require('express');
const app = express();
const port = 8000;

app.use(express.static(__dirname + '/public')).listen(port);
console.log('server running on port ' + port);