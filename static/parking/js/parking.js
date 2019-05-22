let myMap;
let canvas;

const mappa = new Mappa('Leaflet');

// 39.950051, -75.600459
const options = {
	lat:39.951000,
	lng:-75.596800,
	zoom:16,
	style: "http://{s}.tile.osm.org/{z}/{x}/{y}.png"
}


// p5.js setup
function setup(){
	canvas = createCanvas(windowWidth/2,windowHeight/2); 
    // Add a grey background
    // background(100);
    myMap = mappa.tileMap(options);
    myMap.overlay(canvas);
	fill(200, 100, 100);
	myMap.onChange(drawPoints);
}

// p5.js draw
function draw(){
	

}



function update(){
	
}


function drawPoints(){
	clear();
	const nigeria = myMap.latLngToPixel(39.951452, -75.600079);
	ellipse(nigeria.x, nigeria.y, 2,2);
}


// console.log(parking_spots_json)

