import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { Plus, Trash2, Image as ImageIcon, Edit2, Search } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../api';

const AlbumsPage = () => {
  const [albums, setAlbums] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newAlbumName, setNewAlbumName] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [showAlbumDetails, setShowAlbumDetails] = useState(false);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    fetchAlbums();
  }, []);

  const fetchAlbums = async () => {
    setIsLoading(true);
    try {
      const response = await api.getAlbums();
      if (response.success) {
        setAlbums(response.albums || []);
      } else {
        toast.error('Không thể tải danh sách album');
      }
    } catch (error) {
      console.error('Error fetching albums:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateAlbum = async () => {
    if (!newAlbumName.trim()) {
      toast.error('Vui lòng nhập tên album');
      return;
    }

    setIsCreating(true);
    try {
      const response = await api.createAlbum(newAlbumName);
      if (response.success) {
        toast.success('Tạo album thành công!');
        setNewAlbumName('');
        setShowCreateModal(false);
        await fetchAlbums();
      } else {
        toast.error(response.message || 'Không thể tạo album');
      }
    } catch (error) {
      console.error('Error creating album:', error);
      toast.error('Lỗi kết nối server');
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteAlbum = async (albumId) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa album này?')) {
      try {
        const response = await api.deleteAlbum(albumId);
        if (response.success) {
          toast.success('Xóa album thành công!');
          await fetchAlbums();
        } else {
          toast.error(response.message || 'Không thể xóa album');
        }
      } catch (error) {
        console.error('Error deleting album:', error);
        toast.error('Lỗi kết nối server');
      }
    }
  };

  const handleDeleteImage = async (albumId, imageId) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa hình ảnh này?')) {
      try {
        const response = await api.deleteImage(albumId, imageId);
        if (response.success) {
          toast.success('Xóa hình ảnh thành công!');
          await fetchAlbums();
          setSelectedAlbum(null);
        } else {
          toast.error(response.message || 'Không thể xóa hình ảnh');
        }
      } catch (error) {
        console.error('Error deleting image:', error);
        toast.error('Lỗi kết nối server');
      }
    }
  };

  const filteredAlbums = albums.filter((album) =>
    album.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-50 to-pink-100 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-pink-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Album Du Lịch</h1>
            <p className="text-gray-600">Quản lý và lưu trữ hình ảnh du lịch của bạn</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Tạo Album
          </button>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Tìm kiếm album..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
        </div>

        {/* Albums Grid */}
        {filteredAlbums.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <ImageIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-xl text-gray-500 mb-4">Chưa có album nào</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition"
            >
              Tạo album đầu tiên
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAlbums.map((album) => (
              <div
                key={album.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition cursor-pointer"
              >
                <div
                  className="relative h-40 bg-gradient-to-br from-purple-400 to-pink-400"
                  onClick={() => {
                    setSelectedAlbum(album);
                    setShowAlbumDetails(true);
                  }}
                >
                  {album.images && album.images.length > 0 ? (
                    <img
                      src={album.images[0]}
                      alt={album.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <ImageIcon className="w-12 h-12 text-white opacity-50" />
                    </div>
                  )}
                  {album.images && album.images.length > 0 && (
                    <div className="absolute top-2 right-2 bg-white bg-opacity-90 text-sm font-bold px-2 py-1 rounded">
                      {album.images.length} ảnh
                    </div>
                  )}
                </div>

                <div className="p-4">
                  <h3 className="text-lg font-bold text-gray-800 mb-2 truncate">
                    {album.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-4">
                    {album.description || 'Không có mô tả'}
                  </p>
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        setSelectedAlbum(album);
                        setShowAlbumDetails(true);
                      }}
                      className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded transition text-sm"
                    >
                      Xem Chi Tiết
                    </button>
                    <button
                      onClick={() => handleDeleteAlbum(album.id)}
                      className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-3 rounded transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Create Album Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 max-w-md w-full">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Tạo Album Mới</h2>
              <input
                type="text"
                placeholder="Tên album"
                value={newAlbumName}
                onChange={(e) => setNewAlbumName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <div className="flex gap-4">
                <button
                  onClick={handleCreateAlbum}
                  disabled={isCreating}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg transition"
                >
                  {isCreating ? 'Đang tạo...' : 'Tạo'}
                </button>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    setNewAlbumName('');
                  }}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg transition"
                >
                  Hủy
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Album Details Modal */}
        {showAlbumDetails && selectedAlbum && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b flex justify-between items-center sticky top-0 bg-white">
                <h2 className="text-2xl font-bold text-gray-800">{selectedAlbum.name}</h2>
                <button
                  onClick={() => setShowAlbumDetails(false)}
                  className="text-gray-600 hover:text-gray-800 text-2xl"
                >
                  ✕
                </button>
              </div>

              <div className="p-6">
                {selectedAlbum.images && selectedAlbum.images.length > 0 ? (
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {selectedAlbum.images.map((image, index) => (
                      <div key={index} className="relative group">
                        <img
                          src={image}
                          alt={`Album image ${index}`}
                          className="w-full h-48 object-cover rounded-lg"
                        />
                        <button
                          onClick={() =>
                            handleDeleteImage(selectedAlbum.id, index)
                          }
                          className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg opacity-0 group-hover:opacity-100 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <ImageIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">Album trống</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AlbumsPage;
