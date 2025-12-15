/**
 * Avatar Manager - Quản lý hiển thị avatar trên toàn website
 * Tự động load và hiển thị avatar của user đã đăng nhập
 */

(function() {
    'use strict';

    // Load và hiển thị avatar từ localStorage
    function loadUserAvatar() {
        const savedAvatar = localStorage.getItem('userAvatar');
        const userName = localStorage.getItem('userName') || localStorage.getItem('fullname') || 'User';
        const userEmail = localStorage.getItem('userEmail');
        const isLoggedIn = localStorage.getItem('authToken');

        // Tìm tất cả các icon user-circle trong navigation
        const userIcons = document.querySelectorAll('.fa-user-circle');
        
        userIcons.forEach(icon => {
            // Chỉ xử lý icon trong navigation (không phải trong modal login)
            const isInNav = icon.closest('nav') !== null;
            if (!isInNav) return;

            if (savedAvatar && isLoggedIn) {
                // Tạo element img thay thế icon
                const avatarImg = document.createElement('img');
                avatarImg.src = savedAvatar;
                avatarImg.alt = 'Avatar';
                avatarImg.className = 'w-8 h-8 rounded-full object-cover border-2 border-white shadow-sm';
                avatarImg.style.display = 'inline-block';
                
                // Thay thế icon bằng img
                const parent = icon.parentElement;
                if (parent && !parent.querySelector('img.rounded-full')) {
                    parent.replaceChild(avatarImg, icon);
                }
            }
        });

        // Ẩn tên user bên cạnh avatar (chỉ hiển thị avatar)
        const userDisplayName = document.getElementById('userDisplayName');
        if (userDisplayName) {
            userDisplayName.textContent = '';
            userDisplayName.classList.add('hidden');
        }

        // Cập nhật thông tin trong dropdown menu
        // Hỗ trợ nhiều ID khác nhau (navUserName, navUserEmail hoặc userEmail)
        const navUserName = document.getElementById('navUserName');
        const navUserEmail = document.getElementById('navUserEmail');
        const userEmailAlt = document.getElementById('userEmail'); // Fallback ID
        
        // Luôn hiển thị "Hello!" thay vì tên user
        if (navUserName) {
            navUserName.textContent = 'Hello!';
        } else {
            // Tìm element có class text-sm font-semibold và set "Hello!"
            const helloElements = document.querySelectorAll('#userDropdown .text-sm.font-semibold');
            helloElements.forEach(el => {
                el.textContent = 'Hello!';
            });
        }
        
        if (userEmail && isLoggedIn) {
            // Cập nhật email user (thử cả 2 ID)
            if (navUserEmail) {
                navUserEmail.textContent = userEmail;
            } else if (userEmailAlt) {
                userEmailAlt.textContent = userEmail;
            } else {
                // Tìm element có class text-xs text-gray-600 trong dropdown
                const emailElements = document.querySelectorAll('#userDropdown .text-xs.text-gray-600');
                emailElements.forEach(el => {
                    if (!el.textContent || el.textContent.trim() === '') {
                        el.textContent = userEmail;
                    }
                });
            }
        } else {
            // Xóa text nếu không có userEmail
            if (navUserEmail) {
                navUserEmail.textContent = '';
            }
            if (userEmailAlt) {
                userEmailAlt.textContent = '';
            }
        }

        // Show/hide menu dựa trên trạng thái login
        const loggedInMenu = document.getElementById('loggedInMenu');
        const loggedOutMenu = document.getElementById('loggedOutMenu');
        
        if (isLoggedIn) {
            if (loggedInMenu) loggedInMenu.classList.remove('hidden');
            if (loggedOutMenu) loggedOutMenu.classList.add('hidden');
        } else {
            if (loggedInMenu) loggedInMenu.classList.add('hidden');
            if (loggedOutMenu) loggedOutMenu.classList.remove('hidden');
        }
    }

    // Listen for avatar changes across tabs/windows
    window.addEventListener('storage', function(e) {
        if (e.key === 'userAvatar') {
            loadUserAvatar();
        }
    });

    // Load avatar khi DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadUserAvatar);
    } else {
        loadUserAvatar();
    }

    // Export function để có thể gọi từ các trang khác
    window.loadUserAvatar = loadUserAvatar;

    // Reload avatar sau một thời gian ngắn để đảm bảo DOM đã load hoàn toàn
    setTimeout(loadUserAvatar, 100);
})();
