import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { Heart, MapPin, Navigation, Search, Sparkles } from 'lucide-react';
import DestinationCard from '../components/DestinationCard';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../api';

const RecommendPage = () => {
  const [activeTab, setActiveTab] = useState('interest');
  const [interest, setInterest] = useState('');
  const [location, setLocation] = useState({ lat: null, lon: null });
  const [radius, setRadius] = useState(50);
  const [recommendations, setRecommendations] = useState([]);
  const [aiRecommendation, setAiRecommendation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isGettingLocation, setIsGettingLocation] = useState(false);

  // Featured destinations for display
  const featuredDestinations = [
    {
      name: 'Vịnh Hạ Long',
      location: 'Quảng Ninh',
      description: 'Vịnh Hạ Long nổi tiếng với hàng nghìn hòn đảo đá vôi kỳ thú, được UNESCO công nhận là di sản thiên nhiên thế giới.',
      image: 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
    },
    {
      name: 'Phố cổ Hội An',
      location: 'Quảng Nam',
      description: 'Thành phố cổ được UNESCO công nhận là Di sản Văn hóa Thế giới với kiến trúc độc đáo và đèn lồng rực rỡ.',
      image: 'https://images.unsplash.com/photo-1583417267826-aebc4d1542e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
    },
    {
      name: 'Sapa',
      location: 'Lào Cai',
      description: 'Thị trấn miền núi nổi tiếng với ruộng bậc thang tuyệt đẹp và khí hậu mát mẻ quanh năm.',
      image: 'https://images.unsplash.com/photo-1583417267826-aebc4d1542e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
    }
  ];

  const getCurrentLocation = () => {
    setIsGettingLocation(true);
    
    if (!navigator.geolocation) {
      toast.error('Trình duyệt không hỗ trợ định vị');
      setIsGettingLocation(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude
        });
        toast.success('Đã lấy vị trí hiện tại');
        setIsGettingLocation(false);
      },
      (error) => {
        console.error('Error getting location:', error);
        toast.error('Không thể lấy vị trí. Vui lòng kiểm tra quyền truy cập.');
        setIsGettingLocation(false);
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const handleInterestSearch = async () => {
    if (!interest.trim()) {
      toast.error('Vui lòng nhập sở thích của bạn');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.recommendByInterest(interest);
      if (response.success) {
        setRecommendations(response.recommendations || []);
        toast.success(`Tìm thấy ${response.recommendations?.length || 0} gợi ý`);
      } else {
        toast.error('Không tìm thấy gợi ý phù hợp');
      }
    } catch (error) {
      console.error('Error getting recommendations:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAiRecommend = async () => {
    if (!interest.trim()) {
      toast.error('Vui lòng nhập sở thích của bạn');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.aiRecommend(interest);
      if (response.success) {
        setAiRecommendation(response.recommendation);
        toast.success('AI đã đưa ra gợi ý!');
      } else {
        toast.error('Không thể lấy gợi ý từ AI');
      }
    } catch (error) {
      console.error('Error getting AI recommendation:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNearbySearch = async () => {
    if (!location.lat || !location.lon) {
      toast.error('Vui lòng lấy vị trí hiện tại trước');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.recommendNearby(location.lat, location.lon, radius);
      if (response.success) {
        setRecommendations(response.destinations || []);
        toast.success(`Tìm thấy ${response.destinations?.length || 0} điểm gần bạn`);
      } else {
        toast.error('Không tìm thấy điểm nào gần vị trí của bạn');
      }
    } catch (error) {
      console.error('Error getting nearby destinations:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">
              Khám phá điểm đến tuyệt vời
            </h1>
            <p className="text-xl text-blue-100">
              Tìm kiếm địa điểm du lịch phù hợp với sở thích của bạn
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('interest')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'interest'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Heart className="inline-block mr-2 h-4 w-4" />
              Theo sở thích
            </button>
            <button
              onClick={() => setActiveTab('nearby')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'nearby'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <MapPin className="inline-block mr-2 h-4 w-4" />
              Gần tôi
            </button>
            <button
              onClick={() => setActiveTab('ai')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'ai'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Sparkles className="inline-block mr-2 h-4 w-4" />
              AI thông minh
            </button>
          </nav>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Interest-based Recommendations */}
        {activeTab === 'interest' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-6 text-center">
                Gợi ý điểm đến theo sở thích
              </h2>
              <p className="text-gray-600 text-center mb-6">
                Nhập sở thích của bạn để nhận được những gợi ý địa điểm phù hợp
              </p>
              
              <div className="max-w-2xl mx-auto">
                <div className="flex space-x-4">
                  <input
                    type="text"
                    value={interest}
                    onChange={(e) => setInterest(e.target.value)}
                    placeholder="Nhập sở thích của bạn (ví dụ: biển, núi, lịch sử...)"
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    onKeyPress={(e) => e.key === 'Enter' && handleInterestSearch()}
                  />
                  <button
                    onClick={handleInterestSearch}
                    disabled={isLoading}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors flex items-center"
                  >
                    <Search className="h-4 w-4 mr-2" />
                    Tìm kiếm
                  </button>
                </div>
              </div>
            </div>

            {/* Featured Destinations */}
            {recommendations.length === 0 && !isLoading && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-6">Điểm đến nổi bật</h3>
                <div className="grid md:grid-cols-3 gap-6">
                  {featuredDestinations.map((dest, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg overflow-hidden">
                      <img
                        src={dest.image}
                        alt={dest.name}
                        className="w-full h-48 object-cover"
                      />
                      <div className="p-4">
                        <h4 className="font-semibold text-lg mb-2">{dest.name}</h4>
                        <p className="text-sm text-gray-600 mb-2">{dest.location}</p>
                        <p className="text-sm text-gray-700">{dest.description}</p>
                        <button className="mt-3 text-blue-600 text-sm font-medium hover:text-blue-700">
                          Xem chi tiết →
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Results */}
            {isLoading && <LoadingSpinner text="Đang tìm kiếm gợi ý..." />}
            
            {recommendations.length > 0 && !isLoading && (
              <div className="space-y-4">
                <h3 className="text-xl font-semibold">
                  Tìm thấy {recommendations.length} gợi ý cho "{interest}"
                </h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
                      <DestinationCard destination={rec.destination} />
                      {rec.score && (
                        <div className="px-4 pb-4">
                          <div className="flex items-center justify-between text-sm">
                            <span className="text-gray-600">Độ phù hợp:</span>
                            <div className="flex items-center">
                              <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                                <div 
                                  className="bg-blue-600 h-2 rounded-full" 
                                  style={{width: `${Math.min(rec.score * 10, 100)}%`}}
                                ></div>
                              </div>
                              <span className="font-medium">{rec.score}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Nearby Recommendations */}
        {activeTab === 'nearby' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-6 text-center">
                Tìm điểm đến gần bạn
              </h2>
              
              <div className="max-w-2xl mx-auto space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Vị trí hiện tại:</p>
                    {location.lat && location.lon ? (
                      <p className="text-sm text-green-600">
                        Lat: {location.lat.toFixed(6)}, Lon: {location.lon.toFixed(6)}
                      </p>
                    ) : (
                      <p className="text-sm text-gray-500">Chưa xác định</p>
                    )}
                  </div>
                  <button
                    onClick={getCurrentLocation}
                    disabled={isGettingLocation}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors flex items-center"
                  >
                    <Navigation className="h-4 w-4 mr-2" />
                    {isGettingLocation ? 'Đang lấy vị trí...' : 'Lấy vị trí'}
                  </button>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Bán kính tìm kiếm: {radius} km
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="100"
                    value={radius}
                    onChange={(e) => setRadius(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <button
                  onClick={handleNearbySearch}
                  disabled={isLoading || !location.lat}
                  className="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors flex items-center justify-center"
                >
                  <MapPin className="h-4 w-4 mr-2" />
                  Tìm điểm gần tôi
                </button>
              </div>
            </div>

            {/* Nearby Results */}
            {isLoading && <LoadingSpinner text="Đang tìm điểm đến gần bạn..." />}
            
            {recommendations.length > 0 && !isLoading && (
              <div className="space-y-4">
                <h3 className="text-xl font-semibold">
                  Tìm thấy {recommendations.length} điểm trong bán kính {radius} km
                </h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((dest, index) => (
                    <DestinationCard 
                      key={index} 
                      destination={dest} 
                      showDistance={true}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* AI Recommendations */}
        {activeTab === 'ai' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-6 text-center">
                Gợi ý thông minh từ AI
              </h2>
              <p className="text-gray-600 text-center mb-6">
                AI sẽ phân tích sở thích của bạn và đưa ra lời khuyên chi tiết
              </p>
              
              <div className="max-w-2xl mx-auto space-y-4">
                <textarea
                  value={interest}
                  onChange={(e) => setInterest(e.target.value)}
                  placeholder="Mô tả chi tiết sở thích du lịch của bạn (ví dụ: Tôi thích những nơi yên tĩnh, có biển đẹp và ẩm thực ngon...)"
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={handleAiRecommend}
                  disabled={isLoading}
                  className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-400 transition-colors flex items-center justify-center"
                >
                  <Sparkles className="h-4 w-4 mr-2" />
                  Hỏi AI
                </button>
              </div>
            </div>

            {/* AI Response */}
            {isLoading && <LoadingSpinner text="AI đang phân tích..." />}
            
            {aiRecommendation && !isLoading && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <Sparkles className="h-5 w-5 mr-2 text-purple-600" />
                  Gợi ý từ AI
                </h3>
                <div className="prose max-w-none">
                  <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
                    <pre className="whitespace-pre-wrap font-sans text-gray-800">
                      {aiRecommendation}
                    </pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendPage;