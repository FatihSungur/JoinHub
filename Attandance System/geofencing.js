// Okulun koordinatları (enlem, boylam)
const schoolCoordinates = {
    lat: -75.140224,  // İstanbul Üniversitesi'nin enlemi
    lon: 30.7342592   // İstanbul Üniversitesi'nin boylamı
};

// Mesafe hesaplamak için Haversine formülü (km cinsinden)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Dünya'nın yarıçapı (km)
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // km cinsinden mesafe
}

// Dereceyi radiana dönüştürme fonksiyonu
function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

// Konum bilgisini al ve ekrana yazdır
function locationReceived(position) {
    const userLat = position.coords.latitude;
    const userLon = position.coords.longitude;

    // Kullanıcının konum bilgilerini ekrana yazdır
    const latLonElement = document.getElementById("latlon");
    latLonElement.innerHTML = `Latitude: ${userLat}, Longitude: ${userLon}`;

    // Kullanıcı ile okul arasındaki mesafeyi hesapla
    const distance = calculateDistance(schoolCoordinates.lat, schoolCoordinates.lon, userLat, userLon);

    // 500 metreye kadar okula yakınsa, siteyi kullanmaya izin ver
    if (distance < 0.5) {  // 0.5 km (500 metre)
        console.log("Okul sınırları içindesiniz.");
    } else {
        alert("Okul sınırları dışında. Siteye erişim engelleniyor.");
        window.location.href = "https://www.google.com";  // Başka bir sayfaya yönlendir
    }
}

// Konum bilgisi alınamazsa hata mesajı göster
function locationError(error) {
    alert("Konum bilgisi alınamadı. Lütfen konum servislerinizi açın.");
}

// Konum verisi almak için fonksiyon
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(locationReceived, locationError);
    } else {
        alert("Geolocation API desteklenmiyor.");
    }
}

// Sayfa yüklendiğinde konum verisi al
window.onload = getLocation;