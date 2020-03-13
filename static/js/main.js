$(document).ready(function() {

    /* Hide any notifications after 2.5 seconds */
    setTimeout(() => {
        $("div.alert").hide("slow")
    }, 3500)
    
});

/**
 * Calculate geographical distence between points on sphere
 * http://en.wikipedia.org/wiki/Haversine_formula
 */
function distanceBetweenPoints(lat1, lng1, lat2, lng2) {
    var R = 6371; // equtarial radius
    var radLat1 = lat1 * (Math.PI / 180);
    var radLat2 = lat2 * (Math.PI / 180);
    var deltaLat = (lat2 - lat1) * (Math.PI / 180);
    var deltaLon = (lng2 - lng1) * (Math.PI / 180);
    var a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
            Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2) * 
            Math.cos(radLat1) * Math.cos(radLat2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}