// Login formunu dinle
document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Sayfanın yenilenmesini önle

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        // Backend'e POST isteği gönder
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                alert("Login successful!");
                document.getElementById("loginSection").style.display = "none"; // Login formunu gizle
                document.getElementById("qrSection").style.display = "block";  // QR formunu göster
            } else {
                alert("Invalid username or password!");
            }
        } else {
            alert("Sunucu hatası! Lütfen daha sonra tekrar deneyin.");
        }
    } catch (error) {
        console.error("Hata:", error);
        alert("Sunucuya bağlanılamadı.");
    }
});

// Formun submit olayını dinle
document.getElementById("qrForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Sayfanın yeniden yüklenmesini önler

    // Formdan gelen verileri al
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const student_id = document.getElementById("student_id").value;

    try {
        // Flask API'ye POST isteği gönder
        const response = await fetch("http://127.0.0.1:5000/generate_qr", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, surname, student_id })
        });

        // API'den dönen yanıtı işle
        if (response.ok) {
            const data = await response.blob(); // Görsel veri olarak QR kodu al
            const qrImage = document.getElementById("qrImage");
            const studentName = document.getElementById("student-name");

            // QR kod ve öğrenci ismini göster
            qrImage.src = URL.createObjectURL(data);
            qrImage.style.display = "block";
            studentName.textContent = `${name} ${surname}`;
        } else {
            alert("QR kod oluşturulamadı. Lütfen tekrar deneyin.");
        }
    } catch (error) {
        console.error("Bir hata oluştu:", error);
        alert("Sunucuya bağlanılamadı.");
    }
});
function moveBackgroundText() {
    const backgroundText = document.getElementById("background-text");

    // Ekran boyutlarını al
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Yazının boyutunu al
    const textWidth = backgroundText.offsetWidth;
    const textHeight = backgroundText.offsetHeight;

    // Rastgele pozisyon oluştur (tam ekran sınırlarını kullanarak)
    const randomX = Math.random() * (screenWidth - textWidth);
    const randomY = Math.random() * (screenHeight - textHeight);

    // Yeni pozisyona taşı
    backgroundText.style.left = `${randomX}px`;
    backgroundText.style.top = `${randomY}px`;
}

// Yazıyı her 1 saniyede bir hareket ettir
setInterval(moveBackgroundText, 1000);

