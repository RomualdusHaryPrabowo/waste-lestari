/**
 * EcoSort AI — Classification Page JavaScript
 * Drag & Drop, Image Preview, Prediction API
 */

document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const predictBtn = document.getElementById('predictBtn');
    const removeBtn = document.getElementById('removeBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultCard = document.getElementById('resultCard');

    let selectedFile = null;

    // === Drag & Drop ===
    if (uploadArea) {
        ['dragenter', 'dragover'].forEach(event => {
            uploadArea.addEventListener(event, (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(event => {
            uploadArea.addEventListener(event, (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
    }

    // === Handle File Selection ===
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Harap pilih file gambar (PNG, JPG, JPEG).');
            return;
        }

        selectedFile = file;

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            predictBtn.style.display = 'inline-flex';
            uploadArea.style.display = 'none';
            resultCard.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // === Remove Image ===
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            resetForm();
        });
    }

    function resetForm() {
        selectedFile = null;
        fileInput.value = '';
        imagePreview.style.display = 'none';
        predictBtn.style.display = 'none';
        uploadArea.style.display = 'block';
        resultCard.style.display = 'none';
        loadingOverlay.style.display = 'none';
    }

    // === Predict Button ===
    if (predictBtn) {
        predictBtn.addEventListener('click', async () => {
            if (!selectedFile) return;

            // Show loading
            loadingOverlay.style.display = 'block';
            predictBtn.style.display = 'none';
            imagePreview.style.display = 'none';
            resultCard.style.display = 'none';

            // Prepare form data
            const formData = new FormData();
            formData.append('image', selectedFile);

            try {
                const response = await fetch('/classify/api/predict', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    displayResult(data);
                } else {
                    alert('Terjadi kesalahan: ' + (data.error || 'Unknown error'));
                    resetForm();
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Gagal terhubung ke server. Pastikan Flask berjalan.');
                resetForm();
            }
        });
    }

    // === Display Result ===
    function displayResult(data) {
        loadingOverlay.style.display = 'none';

        // Prediction box
        const predBox = document.getElementById('resultPrediction');
        predBox.style.background = `linear-gradient(135deg, ${data.color}, ${adjustColor(data.color, -20)})`;
        predBox.querySelector('.result-label').textContent = data.prediction;
        predBox.querySelector('.result-confidence').textContent = `Confidence: ${data.confidence}%`;

        // Confidence bar
        const confBar = predBox.querySelector('.confidence-bar');
        confBar.style.width = '0%';
        setTimeout(() => {
            confBar.style.width = `${data.confidence}%`;
        }, 100);

        // Emoji
        const emojiMap = {
            'battery': '🔋', 'biological': '🌱', 'cardboard': '📦',
            'clothes': '👕', 'glass': '🥃', 'metal': '🔩',
            'paper': '📄', 'plastic': '🧴', 'shoes': '👟', 'trash': '🗑️'
        };
        predBox.querySelector('.result-emoji').textContent = emojiMap[data.class_key] || '♻️';

        // Top 3
        const top3Container = document.getElementById('top3Predictions');
        top3Container.innerHTML = '<h4>Top 3 Prediksi</h4>';
        data.top3.forEach((pred, i) => {
            const item = document.createElement('div');
            item.className = 'prediction-item';
            item.innerHTML = `
                <span class="prediction-name">#${i + 1} ${pred.class}</span>
                <span class="prediction-score">${pred.confidence}%</span>
            `;
            top3Container.appendChild(item);
        });

        // Show result
        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Show reset button
        predictBtn.textContent = 'Klasifikasi Ulang';
        predictBtn.style.display = 'inline-flex';
    }

    // === Helper: Adjust Color ===
    function adjustColor(hex, amount) {
        hex = hex.replace('#', '');
        const r = Math.min(255, Math.max(0, parseInt(hex.substring(0, 2), 16) + amount));
        const g = Math.min(255, Math.max(0, parseInt(hex.substring(2, 4), 16) + amount));
        const b = Math.min(255, Math.max(0, parseInt(hex.substring(4, 6), 16) + amount));
        return `rgb(${r}, ${g}, ${b})`;
    }
});