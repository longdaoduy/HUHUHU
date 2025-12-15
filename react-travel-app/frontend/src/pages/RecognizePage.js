import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import { Camera, Upload, Loader } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../api';

const RecognizePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [recognitionResult, setRecognitionResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Vui lòng chọn một tệp hình ảnh');
      return;
    }

    setSelectedFile(file);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleRecognize = async () => {
    if (!selectedFile) {
      toast.error('Vui lòng chọn một hình ảnh');
      return;
    }

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await api.recognizeDestination(formData);
      
      if (response.success) {
        setRecognitionResult(response.data);
        toast.success('Nhận diện thành công!');
      } else {
        toast.error(response.message || 'Không thể nhận diện điểm đến');
      }
    } catch (error) {
      console.error('Error recognizing destination:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setRecognitionResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Camera className="w-12 h-12 text-indigo-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Nhận Diện Điểm Đến</h1>
          <p className="text-gray-600">
            Tải lên một hình ảnh để nhận diện điểm đến du lịch
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-6">
          {!selectedFile ? (
            <div className="flex flex-col items-center">
              <label className="w-full cursor-pointer">
                <div
                  className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-indigo-300 rounded-xl hover:bg-indigo-50 transition"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload className="w-12 h-12 text-indigo-500 mb-2" />
                  <p className="text-lg font-medium text-gray-700">
                    Nhấp để tải lên hoặc kéo thả
                  </p>
                  <p className="text-sm text-gray-500">
                    Hỗ trợ PNG, JPG, GIF (tối đa 5MB)
                  </p>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </label>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-64 object-cover rounded-lg"
                />
              </div>
              <p className="text-sm text-gray-600">
                Tệp: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)}MB)
              </p>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        {selectedFile && (
          <div className="flex gap-4 mb-6">
            <button
              onClick={handleRecognize}
              disabled={isLoading}
              className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Đang xử lý...
                </>
              ) : (
                <>
                  <Camera className="w-5 h-5" />
                  Nhận Diện
                </>
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={isLoading}
              className="flex-1 bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 text-gray-800 font-bold py-3 px-6 rounded-lg transition"
            >
              Xóa
            </button>
          </div>
        )}

        {!selectedFile && !recognitionResult && (
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2"
          >
            <Upload className="w-5 h-5" />
            Tải Lên Hình Ảnh
          </button>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center">
            <LoadingSpinner />
          </div>
        )}

        {/* Recognition Result */}
        {recognitionResult && (
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Kết Quả Nhận Diện</h2>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-2">
                  Điểm Đến
                </label>
                <p className="text-2xl font-bold text-indigo-600">
                  {recognitionResult.destination_name || 'Không xác định'}
                </p>
              </div>

              {recognitionResult.description && (
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Mô Tả
                  </label>
                  <p className="text-gray-700">
                    {recognitionResult.description}
                  </p>
                </div>
              )}

              {recognitionResult.location && (
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Vị Trí
                  </label>
                  <p className="text-gray-700">
                    {recognitionResult.location}
                  </p>
                </div>
              )}

              {recognitionResult.confidence && (
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Độ Chính Xác
                  </label>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-indigo-600 h-2 rounded-full"
                      style={{
                        width: `${(recognitionResult.confidence * 100) || 0}%`,
                      }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {Math.round((recognitionResult.confidence || 0) * 100)}%
                  </p>
                </div>
              )}
            </div>

            <div className="flex gap-4">
              <button
                onClick={handleClear}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition"
              >
                Nhận Diện Hình Ảnh Khác
              </button>
              <button
                onClick={() => window.history.back()}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-3 px-6 rounded-lg transition"
              >
                Quay Lại
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecognizePage;
