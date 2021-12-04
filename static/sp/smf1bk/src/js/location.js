(function($) {
	//获取当前房源的出售状态,设置不同的状态背景图
	var imgsrc;
	var flag = $('body').attr('saled');
	// if(flag == "no") {
		imgsrc = "http://www.webmainland.com/static/sp/smf1/src/img/map-icon.png";
	// } else if(flag == "yes") {
	// 	imgsrc = "/static/sp/img/label_yes.png";
	// }else if(flag == "rent"){
	// 	imgsrc = "/static/sp/img/label_rent.png";
	// }else if(flag == "dark"){
    //     imgsrc = "/static/sp/img/label_dark.png";
    // }else if(flag == "presale"){
    //     imgsrc = "/static/sp/img/label_presale.png";
    // }

	$.fn.mapmarker = function(center, price, address, zoom, latlng) {
		var opts = $.extend({}, $.fn.mapmarker.defaults, {
			"center": center,
			"price": price,
			"address": address,
			"zoom": zoom,
			
		});
		return this.each(function() {
			var map_element = this;
			addMapMarker(map_element, opts.center, opts.price, opts.address, opts.zoom, latlng);
		});
	};

	//默认值  地图中心、价格、地址、缩放倍数
	$.fn.mapmarker.defaults = {
		"center": "Vancouver",
		"price": '0',
		"address": "Vancouver",
		"zoom": 10,
	};

	//创建标记
	function addMapMarker(map_element, center, price, address, zoom, latlng) {
		var myOptions = {
			zoom: zoom,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		
		var map = new google.maps.Map(map_element, myOptions);
		var styledMapType = new google.maps.StyledMapType(
            [
              {
                featureType: 'administrative',
                elementType: 'geometry.stroke',
                stylers: [{color: '#ecebeb'}]
              },
              {
                featureType: 'administrative.land_parcel',
                elementType: 'geometry.stroke',
                stylers: [{color: '#ecebeb'}]
              },
              {
                featureType: 'administrative.land_parcel',
                elementType: 'labels.text.fill',
                stylers: [{color: '#ecebeb'}]
              },
              {
                featureType: 'landscape.natural',
                elementType: 'geometry',
                stylers: [{color: '#ecebeb'}]
              },
              {
                featureType: 'poi',
                elementType: 'geometry',
                stylers: [{color: '#000'}]
              },
              {
                featureType: 'poi',
                elementType: 'labels.text.fill',
                stylers: [{color: '#000'}]
              },
              {
                featureType: 'poi.park',
                elementType: 'geometry.fill',
                stylers: [{color: '#e1e1e1'}]
              },
              {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{color: '#000'}]
              },
              {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{color: '#c2c2c2'}]
              },
              {
                featureType: 'transit.line',
                elementType: 'geometry',
                stylers: [{color: '#d5d5d5'}]
              },
              {
                featureType: 'transit.line',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d5d5d5'}]
              },
              {
                featureType: 'transit.line',
                elementType: 'labels.text.stroke',
                stylers: [{color: '#c3c2c2'}]
              },
              {
                featureType: 'transit.station',
                elementType: 'geometry',
                stylers: [{color: '#c3c2c2'}]
              },
              {
                featureType: 'water',
                elementType: 'geometry.fill',
                stylers: [{color: '#c3c2c2'}]
              },
              {
                featureType: 'water',
                elementType: 'labels.text.fill',
                stylers: [{color: '#c3c2c2'}]
              }
            ],
            {name: 'Styled Map'});
		map.mapTypes.set('styled_map', styledMapType);
        map.setMapTypeId('styled_map');
		var geocoder = new google.maps.Geocoder();
		var locationLa;
		geocoder.geocode({
			'address': center,
			'region': 'ca'
		}, function(results, status) {
			if(status == google.maps.GeocoderStatus.OK) {

				//优先使用录入的经纬度
				if(!latlng.lat){
					console.log('aaa')
					locationLa = results[0].geometry.location;
				}else{
					console.log('bbb')
					locationLa = latlng
				}
				console.log(locationLa)
				map.setCenter(locationLa);
			} else {
				console.log(latlng)
				map.setCenter(latlng);
				console.log("Geocode was not successful for the following reason: " + status);
			}
		});
		//地图缩放监听事件  保证缩放时当前房源一直地图中心
		google.maps.event.addListener(map, 'zoom_changed', function() {
			map.setCenter(locationLa);
		});

		geocoder.geocode({
			"address": address,
			'region': 'ca'
		}, function(results, status) {
			if(status == 'OK' || latlng.lat) {
				var latitude = latlng.lat?latlng.lat:results[0].geometry.location.lat();
				var longitude = latlng.lat?latlng.lng:results[0].geometry.location.lng();
				//在回调函数中通过地址获取经纬度坐标，实现marker的创建
				var marker = new google.maps.Marker({
					map: map,
					position: new google.maps.LatLng(latitude, longitude),
					animation: google.maps.Animation.DROP,
					icon: {
						//						url: "/static/sp/img/label.png",//地图标记点图片
						url: imgsrc,
					}
					
				});
				google.maps.event.addListener(marker, 'click', function() {
					//TODO  地图标记点点击事件
				});
			}
		});
	}

})(jQuery);