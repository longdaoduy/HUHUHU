import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Eye, EyeOff, UserPlus, Mail, Lock, User, Phone } from 'lucide-react';
import api from '../api';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    fullname: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [agreeTerms, setAgreeTerms] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    if (token) {
      navigate('/');
    }
  }, [navigate]);

  const checkPasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[@$!%*?&]+/)) strength++;
    setPasswordStrength(strength);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (name === 'password') {
      checkPasswordStrength(value);
    }
  };

  const validateForm = () => {
    const { fullname, email, password, confirmPassword } = formData;

    if (!fullname.trim()) {
      toast.error('Vui lòng nhập họ và tên');
      return false;
    }

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

    if (password !== confirmPassword) {
      toast.error('Mật khẩu xác nhận không khớp');
      return false;
    }

    if (!agreeTerms) {
      toast.error('Bạn phải đồng ý với Điều khoản dịch vụ');
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
      const response = await api.register({
        fullname: formData.fullname,
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
      });

      if (response.success) {
        toast.success('Đăng ký thành công! Vui lòng đăng nhập.');
        
        // Redirect to login page
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        toast.error(response.message || 'Email đã tồn tại hoặc có lỗi xảy ra');
      }
    } catch (error) {
      console.error('Signup error:', error);
      toast.error('Lỗi kết nối server. Vui lòng thử lại sau.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialSignup = (provider) => {
    toast.info(`Đăng ký với ${provider} sẽ được hỗ trợ sớm`);
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

  const getPasswordStrengthInfo = () => {
    const strengths = [
      { level: 0, text: 'Chưa nhập', color: 'bg-gray-300' },
      { level: 1, text: 'Yếu', color: 'bg-red-500' },
      { level: 2, text: 'Trung bình', color: 'bg-yellow-500' },
      { level: 3, text: 'Tốt', color: 'bg-blue-500' },
      { level: 4, text: 'Rất tốt', color: 'bg-green-500' },
      { level: 5, text: 'Tuyệt vời', color: 'bg-green-600' },
    ];
    return strengths[passwordStrength] || strengths[0];
  };

  const strengthInfo = getPasswordStrengthInfo();

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation Bar */}
      <nav className="bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4">
          {/* Top Bar */}
          <div className="flex justify-between items-center py-4 border-b border-pink-700">
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
              <a href="#" className="hover:text-pink-200 transition">About us</a>
              <a href="#" className="hover:text-pink-200 transition">Information</a>
              <a href="#" className="hover:text-pink-200 transition">Contact us</a>
            </div>
          </div>

          {/* Menu Bar */}
          <div className="flex justify-between items-center py-3">
            <div className="flex items-center space-x-2">
              <img src="https://via.placeholder.com/40x40/c084fc/ffffff?text=VN" alt="Logo" className="rounded-full" />
              <span className="font-semibold">ECOUTURE</span>
            </div>
            <div className="flex space-x-8 items-center">
              <a href="/" className="hover:text-pink-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Home</a>
              <a href="/recommend" className="hover:text-pink-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Recommendation</a>
              <a href="/recognize" className="hover:text-pink-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Scan image</a>
              <a href="/albums" className="hover:text-pink-200 py-2 border-b-2 border-transparent hover:border-white transition-all">Album</a>
              <div className="relative group">
                <button className="flex items-center space-x-2 hover:text-pink-200 cursor-pointer py-2" onClick={toggleUserMenu}>
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

      {/* Signup Content */}
      <div className="flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-12 text-center">
              <UserPlus className="w-12 h-12 mx-auto mb-4" />
              <h1 className="text-3xl font-bold">Đăng Ký</h1>
              <p className="text-purple-100 mt-2">Tạo tài khoản mới của bạn</p>
            </div>

            {/* Form */}
            <div className="px-8 py-8">
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Full Name Input */}
                <div>
                  <label htmlFor="fullname" className="block text-gray-700 font-semibold mb-2">
                    <User className="inline w-4 h-4 mr-2" />
                    Họ và Tên
                  </label>
                  <input
                    type="text"
                    id="fullname"
                    name="fullname"
                    value={formData.fullname}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                    placeholder="Nguyễn Văn A"
                    disabled={isLoading}
                  />
                </div>

                {/* Email Input */}
                <div>
                  <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">
                    <Mail className="inline w-4 h-4 mr-2" />
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                    placeholder="your@email.com"
                    disabled={isLoading}
                  />
                </div>

                {/* Phone Input */}
                <div>
                  <label htmlFor="phone" className="block text-gray-700 font-semibold mb-2">
                    <Phone className="inline w-4 h-4 mr-2" />
                    Số điện thoại (tuỳ chọn)
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                    placeholder="0123456789"
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
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
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
                  {formData.password && (
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${strengthInfo.color}`}
                          style={{ width: `${(passwordStrength / 5) * 100}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">
                        Độ mạnh: <span className="font-semibold">{strengthInfo.text}</span>
                      </p>
                    </div>
                  )}
                </div>

                {/* Confirm Password Input */}
                <div>
                  <label htmlFor="confirmPassword" className="block text-gray-700 font-semibold mb-2">
                    <Lock className="inline w-4 h-4 mr-2" />
                    Xác nhận mật khẩu
                  </label>
                  <div className="relative">
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      id="confirmPassword"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                      placeholder="••••••••"
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      disabled={isLoading}
                    >
                      {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                {/* Terms Agreement */}
                <div className="flex items-start pt-2">
                  <input
                    type="checkbox"
                    id="terms"
                    checked={agreeTerms}
                    onChange={(e) => setAgreeTerms(e.target.checked)}
                    className="w-4 h-4 text-purple-600 rounded focus:ring-2 focus:ring-purple-500 mt-1"
                    disabled={isLoading}
                  />
                  <label htmlFor="terms" className="ml-2 text-gray-700 text-sm">
                    Tôi đồng ý với{' '}
                    <a href="#" className="text-purple-600 hover:text-purple-800">
                      Điều khoản dịch vụ
                    </a>{' '}
                    và{' '}
                    <a href="#" className="text-purple-600 hover:text-purple-800">
                      Chính sách bảo mật
                    </a>
                  </label>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 rounded-lg transition flex items-center justify-center gap-2 mt-6"
                >
                  {isLoading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Đang xử lý...
                    </>
                  ) : (
                    <>
                      <UserPlus className="w-5 h-5" />
                      Đăng Ký
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Divider */}
            <div className="relative px-8 py-2">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Hoặc</span>
              </div>
            </div>

            {/* Social Signup Buttons */}
            <div className="px-8 py-4 space-y-3">
              <button
                type="button"
                onClick={() => handleSocialSignup('Google')}
                className="w-full border border-gray-300 text-gray-700 font-semibold py-2 rounded-lg hover:bg-gray-50 transition flex items-center justify-center gap-2"
                disabled={isLoading}
              >
                <i className="fab fa-google text-red-600"></i>
                Google
              </button>
              <button
                type="button"
                onClick={() => handleSocialSignup('Facebook')}
                className="w-full border border-gray-300 text-gray-700 font-semibold py-2 rounded-lg hover:bg-gray-50 transition flex items-center justify-center gap-2"
                disabled={isLoading}
              >
                <i className="fab fa-facebook text-blue-600"></i>
                Facebook
              </button>
            </div>

            {/* Footer */}
            <div className="bg-gray-50 px-8 py-6 text-center border-t">
              <p className="text-gray-600">
                Đã có tài khoản?{' '}
                <a href="/login" className="text-purple-600 hover:text-purple-800 font-bold">
                  Đăng nhập tại đây
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

export default SignupPage;
