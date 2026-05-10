from flask import Blueprint, render_template

education_bp = Blueprint("education", __name__)

CATEGORIES = [
    {
        "key": "battery",
        "name": "Baterai",
        "icon": "🔋",
        "description": "Baterai bekas mengandung bahan kimia berbahaya seperti merkuri, timbal, dan kadmium.",
        "examples": [
            "Baterai AA / AAA",
            "Baterai HP / Laptop",
            "Baterai mobil listrik",
            "Baterai kancing (coin cell)",
        ],
        "impact": "Logam berat dari baterai dapat mencemari tanah dan air tanah, membahayakan ekosistem dan kesehatan manusia.",
        "disposal": "Kumpulkan di tempat khusus daur ulang baterai. Jangan buang ke tempat sampah biasa. Hubungi fasilitas pengelolaan limbah B3 terdekat.",
        "color": "#e74c3c",
    },
    {
        "key": "biological",
        "name": "Biologis / Organik",
        "icon": "🌱",
        "description": "Sampah organik berasal dari makhluk hidup dan mudah terurai secara alami.",
        "examples": [
            "Sisa makanan",
            "Kulit buah & sayur",
            "Daun kering",
            "Tulang & kulit ikan",
        ],
        "impact": "Jika tidak dikelola, sampah organik menghasilkan gas metana di TPA yang memperparah pemanasan global.",
        "disposal": "Komposkan di rumah untuk pupuk tanaman. Gunakan metode bokashi atau vermicomposting. Bisa juga dijadikan biogas.",
        "color": "#27ae60",
    },
    {
        "key": "cardboard",
        "name": "Karton",
        "icon": "📦",
        "description": "Karton adalah bahan kemasan yang terbuat dari kertas tebal berlapis, sangat bisa didaur ulang.",
        "examples": [
            "Kardus bekas pengiriman",
            "Kotak makanan",
            "Kemasan elektronik",
            "Kotak sepatu",
        ],
        "impact": "Karton yang terbuang meningkatkan volume sampah di TPA dan menyebabkan deforestasi jika diproduksi terus-menerus.",
        "disposal": "Lipat dan kumpulkan kardus bersih. Bawa ke bank sampah atau pusat daur ulang. Jangan campur dengan sampah basah.",
        "color": "#f39c12",
    },
    {
        "key": "clothes",
        "name": "Pakaian",
        "icon": "👕",
        "description": "Pakaian bekas termasuk sampah tekstil yang membutuhkan penanganan khusus.",
        "examples": [
            "Baju bekas tidak terpakai",
            "Celana sobek",
            "Kain perca",
            "Sepatu & tas tekstil",
        ],
        "impact": "Industri fast fashion menghasilkan jutaan ton limbah tekstil yang sulit terurai dan mencemari lingkungan.",
        "disposal": "Donasikan ke organisasi amal. Daur ulang menjadi kain lap atau bahan isolasi. Jangan buang ke saluran air.",
        "color": "#9b59b6",
    },
    {
        "key": "glass",
        "name": "Kaca",
        "icon": "🥃",
        "description": "Kaca adalah material yang bisa didaur ulang 100% tanpa kehilangan kualitas.",
        "examples": [
            "Botol minuman kaca",
            "Toples selai",
            "Pecahan kaca jendela",
            "Gelas kaca",
        ],
        "impact": "Kaca butuh ribuan tahun untuk terurai di alam. Pecahan kaca bisa membahayakan hewan dan manusia.",
        "disposal": "Bersihkan dan keringkan sebelum didaur ulang. Kumpulkan berdasarkan warna kaca. Bungkus pecahan kaca dengan koran.",
        "color": "#1abc9c",
    },
    {
        "key": "metal",
        "name": "Logam",
        "icon": "🔩",
        "description": "Sampah logam mencakup aluminium, besi, baja, dan tembaga yang sangat bernilai untuk daur ulang.",
        "examples": [
            "Kaleng minuman",
            "Kuningan & tembaga",
            "Aluminium foil",
            "Paku & baut bekas",
        ],
        "impact": "Pertambangan logam baru merusak lingkungan. Daur ulang logam menghemat hingga 95% energi dibanding produksi baru.",
        "disposal": "Kumpulkan di bank sampah. Logam bisa dijual karena memiliki nilai ekonomi tinggi. Pisahkan dari sampah lain.",
        "color": "#3498db",
    },
    {
        "key": "paper",
        "name": "Kertas",
        "icon": "📄",
        "description": "Kertas adalah material yang sangat mudah didaur ulang dan berasal dari sumber daya terbarukan.",
        "examples": [
            "Kertas HVS bekas",
            "Koran & majalah",
            "Kardus tipis",
            "Buku bekas",
        ],
        "impact": "Produksi kertas dari pohon baru menyebabkan deforestasi. Daur ulang kertas menghemat air dan energi.",
        "disposal": "Jangan campur kertas dengan makanan/minyak. Kumpulkan dan bawa ke bank sampah. Gunakan kertas bolak-balik.",
        "color": "#e67e22",
    },
    {
        "key": "plastic",
        "name": "Plastik",
        "icon": "🧴",
        "description": "Plastik adalah jenis sampah paling berbahaya karena butuh ratusan tahun untuk terurai.",
        "examples": [
            "Botol plastik",
            "Kantong plastik",
            "Kemasan makanan",
            "Sedotan & styrofoam",
        ],
        "impact": "Plastik mencemari lautan, membunuh hewan laut, dan menghasilkan mikroplastik yang masuk ke rantai makanan manusia.",
        "disposal": "Kurangi penggunaan plastik sekali pakai. Cuci dan keringkan sebelum daur ulang. Gunakan alternatif ramah lingkungan.",
        "color": "#2ecc71",
    },
    {
        "key": "shoes",
        "name": "Sepatu",
        "icon": "👟",
        "description": "Sepatu bekas terdiri dari campuran material (karet, kulit, tekstil, plastik) yang sulit dipisahkan.",
        "examples": [
            "Sepatu rusak / sobek",
            "Sandal bekas",
            "Sepatu olahraga",
            "Boots karet",
        ],
        "impact": "Sepatu yang dibuang ke TPA menyumbang limbah besar karena materialnya sulit terurai secara alami.",
        "disposal": "Donasikan sepatu yang masih layak. Bawa ke program daur ulang sepatu khusus. Pisahkan komponen jika memungkinkan.",
        "color": "#8e44ad",
    },
    {
        "key": "trash",
        "name": "Sampah Umum",
        "icon": "🗑️",
        "description": "Sampah residual adalah sampah yang tidak bisa didaur ulang dan harus dibuang ke TPA.",
        "examples": [
            "Tisu bekas",
            "Kemasan multilayer",
            "Popok & pembalut",
            "Kotak makanan berminyak",
        ],
        "impact": "Sampah residual membebani kapasitas TPA dan menghasilkan gas rumah kaca saat terurai tanpa pengelolaan.",
        "disposal": "Minimalkan sampah residual. Buang di tempat sampah residu. Pilih produk dengan kemasan minimal dan ramah lingkungan.",
        "color": "#7f8c8d",
    },
]


@education_bp.route("/")
def education_page():
    return render_template("education.html", categories=CATEGORIES)


@education_bp.route("/<category_key>")
def category_detail(category_key):
    category = next((c for c in CATEGORIES if c["key"] == category_key), None)
    if category is None:
        return render_template("education.html", categories=CATEGORIES)
    return render_template("category.html", category=category, all_categories=CATEGORIES)