/**
 * 地图标记物实体类
 * @param {Object} listingname
 * @param {Object} price
 */
function Marker(listingname, price, detail_url) {
	this.listingname = listingname;
	this.price = price;
	this.detail_url = detail_url;
}