import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Eye, EyeOff, LogIn, Mail, Lock } from 'lucide-react';
import api from '../api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    if (token) {
      navigate('/');
    }

    // Load saved email if "Remember me" was checked
    const savedEmail = localStorage.getItem('savedEmail');
    if (savedEmail) {
      setEmail(savedEmail);
      setRememberMe(true);
    }
  }, [navigate]);

  const validateForm = () => {
    if (!email.trim()) {
      toast.error('Vui lòng nhập email');
      return false;
    }

    if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      toast.error('Email không hợp lệ');
      return false;
    }

    if (!password) {
      toast.error('Vui lòng nhập mật khẩu');
      return false;
    }

    if (password.length < 6) {
      toast.error('Mật khẩu phải có ít nhất 6 ký tự');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.login(email, password);

      if (response.success) {
        // Save token and user info
        localStorage.setItem('authToken', response.token);
        localStorage.setItem('userEmail', email);
        
        // Save email if remember me is checked
        if (rememberMe) {
          localStorage.setItem('savedEmail', email);
        } else {
          localStorage.removeItem('savedEmail');
        }

        toast.success('Đăng nhập thành công!');
        
        // Redirect to home page
        setTimeout(() => {
          navigate('/');
          window.location.reload();
        }, 1500);
      } else {
        toast.error(response.message || 'Email hoặc mật khẩu không chính xác');
      }
    } catch (error) {
      console.error('Login error:', error);
      toast.error('Lỗi kết nối server. Vui lòng thử lại sau.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialLogin = (provider) => {
    toast.info(`Đăng nhập với ${provider} sẽ được hỗ trợ sớm`);
  };

  const toggleUserMenu = () => {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {
      dropdown.classList.toggle('hidden');
    }
  };

  const handleLogout = () => {
    if (window.confirm('Bạn có chắc chắn muốn đăng xuất?')) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      toast.success('Đã đăng xuất thành công!');
      window.location.reload();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation Bar */}
      <nav className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4">
          {/* Top Bar */}
          <div className="flex justify-between items-center py-4 border-b border-blue-700">
            <div className="flex items-center space-x-2">
              <i className="fas fa-home text-xl"></i>
              <h1 className="text-xl font-bold">Vietnam UrbanQuest</h1>
            </div>
            <div className="flex space-x-6 items-center">
              <div className="flex items-center space-x-2">
                <select className="bg-transparent border-none text-white">
                  <option className="text-gray-800">Language</option>
                  <option className="text-gray-800">English</option>
                  <option className="text-gray-800">Tiếng Việt</option>
                </select>
              </div>
              <a href="#" className="hover:text-blue-200 transition">About us</a>
              <a href="#" className="hover:text-blue-200 transition">Information</a>
              <a href="#" className="hover:text-blue-200 transition">Contact us</a>
            </div>
          </div>

          {/* Menu Bar */}
          <div className="flex justify-between items-center py-3">
            <div className="flex items-center space-x-2">
              <img src="https://via.placeholder.com/40x40/4299e1/ffffff?text=VN" alt="Logo" className="rounded-full" />
              <span className="font-semibold">ECOUTURE</span>
            </div>
            <div className="flex space-x-8 items-center">
              <a href="/" className="hover:text-blue-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Home</a>
              <a href="/recommend" className="hover:text-blue-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Recommendation</a>
              <a href="/recognize" className="hover:text-blue-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Scan image</a>
              <a href="/albums" className="hover:text-blue-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Album</a>
              <div className="relative group">
                <button className="flex items-center space-x-2 hover:text-blue-200 cursor-pointer py-2" onClick={toggleUserMenu}>
                  <i className="fas fa-user-circle text-xl"></i>
                  <span id="userDisplayName" className="hidden md:inline text-sm"></span>
                </button>
                <div id="userDropdown" className="hidden absolute right-0 mt-0 w-48 bg-white text-gray-800 rounded-lg shadow-lg py-2 group-hover:block hover:block z-50">
                  <div id="loggedInMenu" className="hidden">
                    <div className="px-4 py-2 border-b">
                      <p className="text-sm font-semibold">Xin chào!</p>
                      <p id="userEmail" className="text-xs text-gray-600"></p>
                    </div>
                    <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                      <i className="fas fa-user mr-2"></i>Hồ sơ
                    </a>
                    <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                      <i className="fas fa-cog mr-2"></i>Cài đặt
                    </a>
                    <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                      <i className="fas fa-heart mr-2"></i>Yêu thích
                    </a>
                    <div className="border-t">
                      <button onClick={handleLogout} className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600">
                        <i className="fas fa-sign-out-alt mr-2"></i>Đăng xuất
                      </button>
                    </div>
                  </div>
                  <div id="loggedOutMenu">
                    <a href="/login" className="block px-4 py-2 hover:bg-gray-100">
                      <i className="fas fa-sign-in-alt mr-2"></i>Đăng nhập
                    </a>
                    <a href="/signup" className="block px-4 py-2 hover:bg-gray-100 border-t">
                      <i className="fas fa-user-plus mr-2"></i>Đăng ký
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Login Content */}
      <div className="flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white px-8 py-12 text-center">
              <LogIn className="w-12 h-12 mx-auto mb-4" />
              <h1 className="text-3xl font-bold">Đăng Nhập</h1>
              <p className="text-blue-100 mt-2">Chào mừng bạn quay trở lại</p>
            </div>

            {/* Form */}
            <div className="px-8 py-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Email Input */}
                <div>
                  <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">
                    <Mail className="inline w-4 h-4 mr-2" />
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                    placeholder="your@email.com"
                    disabled={isLoading}
                  />
                </div>

                {/* Password Input */}
                <div>
                  <label htmlFor="password" className="block text-gray-700 font-semibold mb-2">
                    <Lock className="inline w-4 h-4 mr-2" />
                    Mật khẩu
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                      placeholder="••••••••"
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      disabled={isLoading}
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                {/* Remember Me */}
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="remember"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500"
                    disabled={isLoading}
                  />
                  <label htmlFor="remember" className="ml-2 text-gray-700">
                    Ghi nhớ tôi
                  </label>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 rounded-lg transition flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Đang xử lý...
                    </>
                  ) : (
                    <>
                      <LogIn className="w-5 h-5" />
                      Đăng Nhập
                    </>
                  )}
                </button>
              </form>

              {/* Forgot Password Link */}
              <div className="text-center mt-6">
                <a href="#" className="text-indigo-600 hover:text-indigo-800 font-semibold text-sm">
                  Quên mật khẩu?
                </a>
              </div>

              {/* Divider */}
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Hoặc</span>
                </div>
              </div>

              {/* Social Login Buttons */}
              <div className="space-y-3">
                <button
                  type="button"
                  onClick={() => handleSocialLogin('Google')}
                  className="w-full border border-gray-300 text-gray-700 font-semibold py-2 rounded-lg hover:bg-gray-50 transition flex items-center justify-center gap-2"
                  disabled={isLoading}
                >
                  <i className="fab fa-google text-red-600"></i>
                  Google
                </button>
                <button
                  type="button"
                  onClick={() => handleSocialLogin('Facebook')}
                  className="w-full border border-gray-300 text-gray-700 font-semibold py-2 rounded-lg hover:bg-gray-50 transition flex items-center justify-center gap-2"
                  disabled={isLoading}
                >
                  <i className="fab fa-facebook text-blue-600"></i>
                  Facebook
                </button>
              </div>
            </div>

            {/* Footer */}
            <div className="bg-gray-50 px-8 py-6 text-center border-t">
              <p className="text-gray-600">
                Chưa có tài khoản?{' '}
                <a href="/signup" className="text-indigo-600 hover:text-indigo-800 font-bold">
                  Đăng ký ngay
                </a>
              </p>
            </div>
          </div>

          {/* Back to Home */}
          <div className="text-center mt-6">
            <a href="/" className="text-gray-600 hover:text-gray-800 font-semibold flex items-center justify-center gap-2">
              <i className="fas fa-arrow-left"></i>
              Quay lại trang chủ
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
