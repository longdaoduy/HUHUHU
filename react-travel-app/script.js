// API Configuration
const API_BASE_URL = 'http://192.168.1.6.150:8000';

// Global variables
let currentAlbums = [];
let currentRecommendations = [];

// Utility functions
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="flex justify-center items-center py-8"><i class="fas fa-spinner fa-spin text-2xl text-blue-500"></i><span class="ml-2">Loading...</span></div>';
    }
}

function showError(message) {
    alert('Error: ' + message);
}

function showSuccess(message) {
    alert('Success: ' + message);
}

// API Functions
class TravelAPI {
    static async recognizeLandmark(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/recognize/landmark`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error recognizing landmark:', error);
            throw error;
        }
    }

    static async recognizeLocation(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/recognize/location`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error recognizing location:', error);
            throw error;
        }
    }

    static async getRecommendationsByInterest(interest) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/recommend/interest`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ interest })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting recommendations:', error);
            throw error;
        }
    }

    static async getAIRecommendations(interest) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/recommend/ai`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ interest })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting AI recommendations:', error);
            throw error;
        }
    }

    static async getNearbyRecommendations(latitude, longitude, radius = 50) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/recommend/nearby`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ latitude, longitude, radius })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting nearby recommendations:', error);
            throw error;
        }
    }

    static async getAllDestinations() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/destinations`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting destinations:', error);
            throw error;
        }
    }

    static async createAlbum(albumName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: albumName })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error creating album:', error);
            throw error;
        }
    }

    static async addImagesToAlbum(albumName, files, autoRecognize = true) {
        const formData = new FormData();
        
        for (let file of files) {
            formData.append('files', file);
        }
        formData.append('auto_recognize', autoRecognize);
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/${albumName}/images`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error adding images to album:', error);
            throw error;
        }
    }

    static async getAlbums() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting albums:', error);
            throw error;
        }
    }

    static async getAlbumImages(albumName, includeImages = false) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/${albumName}/images?include_images=${includeImages}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting album images:', error);
            throw error;
        }
    }

    static async deleteAlbum(albumName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/${albumName}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error deleting album:', error);
            throw error;
        }
    }

    static async downloadAlbum(albumName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/${albumName}/download`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return response.blob();
        } catch (error) {
            console.error('Error downloading album:', error);
            throw error;
        }
    }

    static async getAlbumStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/stats`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting album stats:', error);
            throw error;
        }
    }

    static async getAlbumGroupedByLandmark(albumName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/albums/${albumName}/group-by-landmark`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting grouped album:', error);
            throw error;
        }
    }
}

// UI Functions
function renderDestinations(destinations) {
    const destinationsContainer = document.getElementById('destinations-grid') || 
                                  document.querySelector('.grid.md\\:grid-cols-3.gap-8');
    if (!destinationsContainer) return;

    if (!destinations || destinations.length === 0) {
        destinationsContainer.innerHTML = '<div class="col-span-3 text-center text-gray-500 py-8">No recommendations found. Try searching with different interests.</div>';
        return;
    }

    destinationsContainer.innerHTML = destinations.map(dest => `
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <img src="${dest.image || 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'}" 
                 alt="${dest.name}" class="w-full h-48 object-cover">
            <div class="p-6">
                <h3 class="text-xl font-bold mb-2">${dest.name}</h3>
                <p class="text-gray-600 text-sm mb-2"><i class="fas fa-map-marker-alt"></i> ${dest.location || 'Vietnam'}</p>
                <p class="text-gray-600 text-sm mb-4">${(dest.introduction || '').substring(0, 100)}${dest.introduction && dest.introduction.length > 100 ? '...' : ''}</p>
                <div class="flex justify-between items-center mb-4">
                    <div class="text-sm text-yellow-600">
                        <i class="fas fa-star"></i> ${dest.rating || 'N/A'}
                    </div>
                    <div class="text-sm text-blue-600">
                        ${dest.price ? (parseInt(dest.price).toLocaleString() + ' VNĐ') : 'Free'}
                    </div>
                </div>
                <button onclick="showDestinationDetails('${dest.name.replace(/'/g, "\\'")}')" 
                        class="w-full bg-gray-800 text-white py-2 rounded-lg hover:bg-gray-700 transition-colors">
                    View Details
                </button>
            </div>
        </div>
    `).join('');
}

function renderAlbums(albums) {
    const albumsGrid = document.getElementById('albums-grid');
    const albumsLoading = document.getElementById('albums-loading');
    const emptyAlbums = document.getElementById('empty-albums');
    const albumStats = document.getElementById('album-stats');
    
    if (albumsLoading) albumsLoading.classList.add('hidden');
    
    if (!albums || albums.length === 0) {
        if (albumsGrid) albumsGrid.classList.add('hidden');
        if (emptyAlbums) emptyAlbums.classList.remove('hidden');
        if (albumStats) albumStats.classList.add('hidden');
        return;
    }

    if (emptyAlbums) emptyAlbums.classList.add('hidden');
    if (albumsGrid) {
        albumsGrid.classList.remove('hidden');
        albumsGrid.innerHTML = albums.map(album => `
            <div class="album-card bg-white rounded-lg card-shadow p-6">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-3">
                        <div class="bg-purple-100 p-3 rounded-lg">
                            <i class="fas fa-images text-purple-600 text-2xl"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-lg">${album.name}</h3>
                            <p class="text-sm text-gray-500">${album.count || 0} images</p>
                        </div>
                    </div>
                </div>
                <div class="flex space-x-2 mt-4">
                    <button onclick="viewAlbum('${album.name}')" 
                            class="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button onclick="downloadAlbum('${album.name}')" 
                            class="flex-1 bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition-colors">
                        <i class="fas fa-download"></i> Download
                    </button>
                    <button onclick="deleteAlbumById('${album.name}')" 
                            class="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 transition-colors">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    // Update stats if container exists
    if (albumStats) {
        albumStats.classList.remove('hidden');
        const totalImages = albums.reduce((sum, album) => sum + (album.count || 0), 0);
        document.getElementById('stat-albums').textContent = albums.length;
        document.getElementById('stat-images').textContent = totalImages;
        document.getElementById('stat-landmarks').textContent = '-';
    }
}

// Event Handlers
async function handleImageUpload(files, uploadType = 'scan') {
    if (!files || files.length === 0) return;

    const file = files[0];
    
    if (uploadType === 'scan') {
        try {
            showLoading('scan-results');
            
            // Call both landmark and location recognition
            const [landmarkResult, locationResult] = await Promise.all([
                TravelAPI.recognizeLandmark(file),
                TravelAPI.recognizeLocation(file)
            ]);
            
            // Display recognition results
            const resultsContainer = document.querySelector('#scan .flex.space-x-4.mt-6');
            if (resultsContainer) {
                resultsContainer.innerHTML = `
                    <div class="flex-1 bg-green-100 text-green-700 p-4 rounded-lg">
                        <h4 class="font-bold">Recognition Results:</h4>
                        <p><strong>Landmark:</strong> ${landmarkResult.landmark || 'Unknown'}</p>
                        <p><strong>Location:</strong> ${locationResult.location || 'Unknown'}</p>
                        <p><strong>Description:</strong> ${landmarkResult.description || locationResult.description || 'No description available'}</p>
                        <p><strong>Confidence:</strong> ${landmarkResult.confidence || 'N/A'}</p>
                    </div>
                    <button onclick="getRecommendationsFromScan('${landmarkResult.landmark || locationResult.location}')" 
                            class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                        Get Recommendations
                    </button>
                `;
            }
        } catch (error) {
            showError('Failed to analyze image: ' + error.message);
        }
    } else if (uploadType === 'album') {
        // Store file for album creation
        window.pendingAlbumImages = window.pendingAlbumImages || [];
        window.pendingAlbumImages.push(file);
        updateAlbumPreview();
    }
}

function updateAlbumPreview() {
    const images = window.pendingAlbumImages || [];
    const uploadArea = document.querySelector('#album .upload-area');
    
    if (images.length > 0) {
        uploadArea.innerHTML = `
            <div class="grid grid-cols-3 gap-4 mb-4">
                ${images.slice(0, 6).map((file, index) => `
                    <div class="relative">
                        <div class="w-full h-20 bg-gray-200 rounded flex items-center justify-center">
                            <i class="fas fa-image text-gray-400 text-2xl"></i>
                        </div>
                        <div class="text-xs text-center mt-1 truncate">${file.name}</div>
                        <button onclick="removeAlbumImage(${index})" 
                                class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                            ×
                        </button>
                    </div>
                `).join('')}
                ${images.length > 6 ? `<div class="text-center text-gray-500">+${images.length - 6} more</div>` : ''}
            </div>
            <p class="text-center text-gray-600">${images.length} image(s) selected</p>
            <button onclick="triggerAlbumUpload()" class="mt-4 bg-gray-800 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors">
                Add More Images
            </button>
        `;
    }
}

async function handleRecommendationSearch() {
    const interestInput = document.querySelector('#recommendation input[type="text"]') || 
                          document.getElementById('interests-input');
    const interests = interestInput?.value.trim();
    
    if (!interests) {
        showError('Please enter your interests');
        return;
    }
    
    try {
        showLoading('recommendation-results');
        const result = await TravelAPI.getRecommendationsByInterest(interests);
        
        if (result.success && result.recommendations) {
            currentRecommendations = result.recommendations.map(r => r.destination);
            renderDestinations(currentRecommendations);
        } else {
            showError('No recommendations found');
        }
    } catch (error) {
        showError('Failed to get recommendations: ' + error.message);
    }
}

async function handleAlbumCreation() {
    const albumNameInput = document.querySelector('#album input[type="text"]') || 
                           document.getElementById('album-name-input');
    const albumName = albumNameInput?.value.trim();
    const images = window.pendingAlbumImages || [];
    
    if (!albumName) {
        showError('Please enter album name');
        return;
    }
    
    if (images.length === 0) {
        showError('Please add at least one image');
        return;
    }
    
    try {
        // First create the album
        const createResult = await TravelAPI.createAlbum(albumName);
        
        if (!createResult.success) {
            showError(createResult.message || 'Failed to create album');
            return;
        }
        
        // Then add images with auto-recognition
        const addResult = await TravelAPI.addImagesToAlbum(albumName, images, true);
        
        if (addResult.success) {
            showSuccess(`Album created! ${addResult.added_count}/${addResult.total_count} images added`);
            
            if (addResult.errors && addResult.errors.length > 0) {
                console.warn('Some images had errors:', addResult.errors);
            }
            
            // Reset form
            albumNameInput.value = '';
            window.pendingAlbumImages = [];
            updateAlbumPreview();
            loadAlbums();
        } else {
            showError('Failed to add images to album');
        }
    } catch (error) {
        showError('Failed to create album: ' + error.message);
    }
}

// Global Functions (called from HTML)
window.getRecommendationsFromScan = async function(location) {
    try {
        const result = await TravelAPI.getRecommendationsByInterest(location);
        
        if (result.success && result.recommendations) {
            currentRecommendations = result.recommendations.map(r => r.destination);
            
            // Scroll to recommendation section
            const recSection = document.getElementById('recommendation') || 
                              document.querySelector('[href="recommendation.html"]');
            if (recSection) {
                if (recSection.tagName === 'A') {
                    // Navigate to recommendation page
                    window.location.href = 'recommendation.html?interest=' + encodeURIComponent(location);
                } else {
                    recSection.scrollIntoView({ behavior: 'smooth' });
                    setTimeout(() => {
                        renderDestinations(currentRecommendations);
                    }, 1000);
                }
            }
        }
    } catch (error) {
        showError('Failed to get location-based recommendations: ' + error.message);
    }
};

window.showDestinationDetails = function(destinationName) {
    const destination = currentRecommendations.find(d => d.name === destinationName);
    if (destination) {
        const details = `
Destination: ${destination.name}
Location: ${destination.location || 'N/A'}
Rating: ${destination.rating || 'N/A'} ⭐

Introduction:
${destination.introduction || 'No description available'}

Price: ${destination.price ? (parseInt(destination.price).toLocaleString() + ' VNĐ') : 'N/A'}

${destination.review ? 'Review:\n' + destination.review : ''}
        `.trim();
        alert(details);
    }
};

window.removeAlbumImage = function(index) {
    window.pendingAlbumImages = window.pendingAlbumImages || [];
    window.pendingAlbumImages.splice(index, 1);
    updateAlbumPreview();
};

window.viewAlbum = async function(albumName) {
    try {
        const result = await TravelAPI.getAlbumImages(albumName, false);
        if (result.success && result.images) {
            // Display album in modal
            const modal = document.getElementById('album-modal');
            const modalContent = document.getElementById('album-modal-content');
            
            if (modal && modalContent) {
                modalContent.innerHTML = `
                    <h2 class="text-2xl font-bold mb-4">${albumName}</h2>
                    <p class="text-gray-600 mb-4">${result.total} images</p>
                    <div class="grid grid-cols-3 gap-4">
                        ${result.images.map(img => `
                            <div class="border rounded p-2">
                                <div class="bg-gray-200 h-32 flex items-center justify-center mb-2">
                                    <i class="fas fa-image text-gray-400 text-3xl"></i>
                                </div>
                                <p class="text-xs text-gray-600 truncate">${img.filename}</p>
                                <p class="text-xs text-blue-600">${img.landmark || 'N/A'}</p>
                            </div>
                        `).join('')}
                    </div>
                    <div class="mt-4 flex space-x-2">
                        <button onclick="downloadAlbum('${albumName}')" 
                                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <button onclick="closeAlbumModal()" 
                                class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
                            Close
                        </button>
                    </div>
                `;
                modal.classList.remove('hidden');
            } else {
                alert(`Album: ${albumName}\nTotal images: ${result.total}`);
            }
        }
    } catch (error) {
        showError('Failed to load album: ' + error.message);
    }
};

window.closeAlbumModal = function() {
    const modal = document.getElementById('album-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
};

window.triggerAlbumUpload = function() {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.accept = 'image/*';
    input.onchange = function(e) {
        Array.from(e.target.files).forEach(file => {
            handleImageUpload([file], 'album');
        });
    };
    input.click();
};

window.deleteAlbumById = async function(albumName) {
    if (confirm('Are you sure you want to delete this album?')) {
        try {
            const result = await TravelAPI.deleteAlbum(albumName);
            if (result.success) {
                showSuccess('Album deleted successfully');
                loadAlbums();
            } else {
                showError(result.message || 'Failed to delete album');
            }
        } catch (error) {
            showError('Failed to delete album: ' + error.message);
        }
    }
};

window.downloadAlbum = async function(albumName) {
    try {
        const blob = await TravelAPI.downloadAlbum(albumName);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${albumName}.zip`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showSuccess('Album downloaded successfully');
    } catch (error) {
        showError('Failed to download album: ' + error.message);
    }
};

async function loadAlbums() {
    try {
        const result = await TravelAPI.getAlbums();
        if (result.success && result.albums) {
            currentAlbums = Object.values(result.albums);
            renderAlbums(currentAlbums);
        }
    } catch (error) {
        console.error('Failed to load albums:', error);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadAlbums();
    
    // Set up event listeners
    const recommendInput = document.querySelector('#recommendation input[type="text"]');
    if (recommendInput) {
        recommendInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleRecommendationSearch();
            }
        });
    }
    
    // Album creation button
    const addToAlbumBtn = document.querySelector('button:contains("Add to album")');
    if (addToAlbumBtn) {
        addToAlbumBtn.addEventListener('click', handleAlbumCreation);
    }
    
    // Enhanced file upload handling
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach((area, index) => {
        const uploadType = index === 0 ? 'scan' : 'album';
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                if (uploadType === 'scan') {
                    handleImageUpload([files[0]], 'scan');
                } else {
                    Array.from(files).forEach(file => {
                        handleImageUpload([file], 'album');
                    });
                }
            }
        });
    });
    
    // Browse buttons
    document.addEventListener('click', function(e) {
        if (e.target.textContent === 'Browse files') {
            const uploadType = e.target.closest('#scan') ? 'scan' : 'album';
            const input = document.createElement('input');
            input.type = 'file';
            input.multiple = uploadType === 'album';
            input.accept = 'image/*';
            input.onchange = function(event) {
                const files = event.target.files;
                if (files.length > 0) {
                    if (uploadType === 'scan') {
                        handleImageUpload([files[0]], 'scan');
                    } else {
                        Array.from(files).forEach(file => {
                            handleImageUpload([file], 'album');
                        });
                    }
                }
            };
            input.click();
        }
        
        if (e.target.textContent === 'Scan image') {
            // Trigger scan if image is already uploaded
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput && fileInput.files.length > 0) {
                handleImageUpload([fileInput.files[0]], 'scan');
            } else {
                showError('Please upload an image first');
            }
        }
        
        if (e.target.textContent === 'Add to album') {
            handleAlbumCreation();
        }
    });
});
