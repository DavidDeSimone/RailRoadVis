function GlobalMap(divName) {
	this.divName = divName;
	this.pointsArray = [];
	this.onClick = function() { console.log(this); };
	this.point = null;
};

GlobalMap.prototype.setPoints = function(pointsArray) {
	this.pointsArray = pointsArray;
};

GlobalMap.prototype.addPoint = function(pointPair) {
	this.pointsArray.push(pointPair);
};

GlobalMap.prototype.setOnClickListener = function(func) {
	this.onClick = func;
};

GlobalMap.prototype.display = function() {
	var map = L.map(this.divName).setView([31.7, -98.99], 8);

	L.tileLayer('http://{s}.tiles.mapbox.com/v3/djd231.k39lc6co/{z}/{x}/{y}.png', {
             attribution: 'Map data &copy; [...]',
             maxZoom: 18
	}).addTo(map);


	var radiusArray = this._getRRRadiusArray(this.pointsArray);

	for(var i = 0; i < this.pointsArray.length; i++) {
		var point = this.pointsArray[i];
		//var marker = L.marker(point).addTo(map);
		var radius = radiusArray[i];
		var circle = L.circle(point, radius, {
    		color: point.color,
    		//fillColor: point.color,
    		fillOpacity: 0.5
		}).addTo(map);

		circle.name = point[2]; // points are in form [lat, long, name]
		$(circle).on("click", this.onClick);
	}

	this.mapObj = map;
};

GlobalMap.prototype.putItemSelectMarker = function(point) {
	this.point = L.marker(point).addTo(this.mapObj);
}

GlobalMap.prototype.removeItemSelectMarker = function() {
	if(this.point != null) {
		this.mapObj.removeLayer(this.point);
	}
}

GlobalMap.prototype._getRRRadiusArray = function(pointsArray) {
	var max = 0;
	var maxItem = null;
	var radiusArray = [];
	for(var i = 0; i < pointsArray.length; i++) {
		var item = pointsArray[i];
		var str = item[2];
		var strs = str.split("(");
		var strs2 = strs[1].split(")");
		var num = strs2[0];
		item.value = num;

		if(num > max) {
			max = num;
			maxItem = item;
		}
	}

	max = 25
	min = 5;
	var colorArray = []
	for(var i = 5; i < max; i++) {
		colorArray.push(i);
	}

	var color = d3.scale.ordinal()
      .domain(colorArray)
      .range(d3.range(colorArray.length).map(d3.scale.linear()
        .domain([0, colorArray.length - 1])
        .range(["#ff0000", "grey"])
        .interpolate(d3.interpolateHcl)));


	for(var i = 0; i < pointsArray.length; i++) {
		var item = pointsArray[i];
		item.color = color(item.value);
		radiusArray.push((item.value / max) * 2500);
	}

	


	return radiusArray;
}