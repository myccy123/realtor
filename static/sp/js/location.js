(function($) {
	//获取当前房源的出售状态,设置不同的状态背景图
	var imgsrc;
	var flag = $('body').attr('saled');
	if(flag == "no") {
		imgsrc = "/static/sp/img/label.png";
	} else if(flag == "yes") {
		imgsrc = "/static/sp/img/label_yes.png";
	}else{
		imgsrc = "/static/sp/img/label_rent.png";
	}

	$.fn.mapmarker = function(center, price, address, zoom, latlng) {
		console.log('latlng-----------', latlng)
		var opts = $.extend({}, $.fn.mapmarker.defaults, {
			"center": center,
			"price": price,
			"address": address,
			"zoom": zoom
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
		"zoom": 10
	};

	//创建标记
	function addMapMarker(map_element, center, price, address, zoom, latlng) {
		var myOptions = {
			zoom: zoom,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		var map = new google.maps.Map(map_element, myOptions);
		var geocoder = new google.maps.Geocoder();
		var locationLa;
		if (latlng) {
			map.setCenter({lat: latlng[0], lng: latlng[1]})
		} else {
			geocoder.geocode({
				'address': center
			}, function(results, status) {
				if(status == google.maps.GeocoderStatus.OK) {
					locationLa = results[0].geometry.location;
					map.setCenter(results[0].geometry.location);
				} else {
					console.log("Geocode was not successful for the following reason: " + status);
				}
			});
		}
		//地图缩放监听事件  保证缩放时当前房源一直地图中心
		google.maps.event.addListener(map, 'zoom_changed', function() {
			if(latlng) {
				map.setCenter({lat: latlng[0], lng: latlng[1]});
			}else {
				map.setCenter(locationLa);
			}
		});

		geocoder.geocode({
			"address": address
		}, function(results, status) {
			if(status == 'OK') {
				var latitude = results[0].geometry.location.lat();
				var longitude = results[0].geometry.location.lng();
				//在回调函数中通过地址获取经纬度坐标，实现marker的创建
				console.log('latlng---->>', latlng)
				if(latlng) {
					latitude = latlng[0];
					longitude = latlng[1];
				}
				var marker = new google.maps.Marker({
					map: map,
					position: new google.maps.LatLng(latitude, longitude),
					animation: google.maps.Animation.DROP,
					icon: {
						//						url: "/static/sp/img/label.png",//地图标记点图片
						url: imgsrc,
					},
					label: {
						fontFamily: 'STKaiti',
						fontSize: '16px',
						color: '#fa8572',
						fontWeight: 'normal',
						text: price
					}
				});
				google.maps.event.addListener(marker, 'click', function() {
					//TODO  地图标记点点击事件
				});
			}
		});
	}

})(jQuery);