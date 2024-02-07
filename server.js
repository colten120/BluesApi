const express = require('express'),
	path = require('path'),
	app = express(),
	fs = require('node:fs');

app.use(express.urlencoded({extended:true}));

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res) {
	res.redirect('index.html');
});

app.post('/save', function(req,res){ 
	console.log(req.body);
	
	// let formData = {
	
	// } 

	res.send(req.body);  
	let settings = require("./settings.json")

	// STEP 2: add new user data to users object using push method  
	settings.push(req.body) 

	// STEP 3: Writing data in a JSON file 
	fs.writeFile('settings.json', JSON.stringify(settings), err =>{ 
		if(err) throw err; 
		console.log("Done writting JSON file");
	}); 

	// STEP 4: Write the new info in the text file named message

	fs.writeFile('./settings.txt', JSON.stringify(settings), err =>{ 
		if(err) throw err 

		console.log("Done writting text file")
	}); 
});

app.listen(8000);