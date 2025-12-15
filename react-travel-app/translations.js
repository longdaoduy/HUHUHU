// Multilingual translation system
const translations = {
    vi: {
        // Navigation
        home: "Trang Chủ",
        about: "Giới Thiệu",
        information: "Thông Tin",
        scan: "Quét Ảnh",
        recommendation: "Gợi Ý",
        favorites: "Yêu Thích",
        album: "Album",
        chatbot: "Chatbot",
        profile: "Hồ Sơ",
        settings: "Cài Đặt",
        logout: "Đăng Xuất",
        login: "Đăng Nhập",
        signup: "Đăng Ký",
        
        // Common
        language: "Ngôn Ngữ",
        search: "Tìm Kiếm",
        cancel: "Hủy",
        save: "Lưu",
        delete: "Xóa",
        edit: "Sửa",
        create: "Tạo Mới",
        upload: "Tải Lên",
        download: "Tải Xuống",
        close: "Đóng",
        submit: "Gửi",
        back: "Quay Lại",
        next: "Tiếp Theo",
        loading: "Đang Tải...",
        
        // Home Page
        discover_hcmc: "Khám Phá Thành Phố Hồ Chí Minh",
        welcome_message: "Chào mừng đến với ứng dụng du lịch thông minh",
        explore_destinations: "Khám Phá Điểm Đến",
        popular_places: "Địa Điểm Phổ Biến",
        featured_destinations: "Điểm Đến Nổi Bật",
        
        // Scan Page
        scan_landmark: "Quét Địa Danh",
        upload_image: "Tải Ảnh Lên",
        take_photo: "Chụp Ảnh",
        recognize: "Nhận Diện",
        recognition_result: "Kết Quả Nhận Diện",
        confidence: "Độ Tin Cậy",
        landmark_name: "Tên Địa Danh",
        
        // Recommendation
        get_recommendations: "Nhận Gợi Ý",
        your_interests: "Sở Thích Của Bạn",
        nearby_places: "Địa Điểm Gần Đây",
        ai_recommendations: "Gợi Ý AI",
        search_by_interest: "Tìm Theo Sở Thích",
        search_by_location: "Tìm Theo Vị Trí",
        
        // Album
        my_albums: "Album Của Tôi",
        create_album: "Tạo Album",
        album_name: "Tên Album",
        add_images: "Thêm Ảnh",
        view_album: "Xem Album",
        delete_album: "Xóa Album",
        download_zip: "Tải ZIP",
        all_images: "Tất Cả Ảnh",
        group_by_landmark: "Nhóm Theo Địa Danh",
        photo_albums: "Album Ảnh",
        create_album: "Tạo Mới Album",
        
        // Profile
        my_profile: "Hồ Sơ Của Tôi",
        fullname: "Họ Và Tên",
        email: "Email",
        phone: "Số Điện Thoại",
        update_profile: "Cập Nhật Hồ Sơ",
        change_password: "Đổi Mật Khẩu",
        
        // Settings
        app_settings: "Cài Đặt Ứng Dụng",
        notifications: "Thông Báo",
        theme: "Giao Diện",
        light_theme: "Sáng",
        dark_theme: "Tối",
        
        // Authentication
        email_address: "Địa Chỉ Email",
        password: "Mật Khẩu",
        confirm_password: "Xác Nhận Mật Khẩu",
        remember_me: "Ghi Nhớ Đăng Nhập",
        forgot_password: "Quên Mật Khẩu?",
        no_account: "Chưa Có Tài Khoản?",
        have_account: "Đã Có Tài Khoản?",
        
        // Forgot Password
        forgot_password_title: "Đặt Lại Mật Khẩu",
        forgot_password_instruction: "Nhập địa chỉ email của bạn và chúng tôi sẽ gửi mã đặt lại cho bạn.",
        reset_code: "Mã Đặt Lại",
        new_password: "Mật Khẩu Mới",
        confirm_new_password: "Xác Nhận Mật Khẩu Mới",
        send_reset_code: "Gửi Mã Đặt Lại",
        reset_password_btn: "Đặt Lại Mật Khẩu",
        back_to_login: "Quay Lại Đăng Nhập",
        email: "Email",
        
        // Messages
        success: "Thành Công",
        error: "Lỗi",
        warning: "Cảnh Báo",
        please_wait: "Vui Lòng Đợi...",
        no_results: "Không Có Kết Quả",
        
        // Chatbot
        chatbot_title: "Trợ Lý Du Lịch AI",
        type_message: "Nhập Tin Nhắn...",
        send_message: "Gửi",
        clear_chat: "Xóa Lịch Sử",
        
        // Favorites
        my_favorites: "Yêu Thích Của Tôi",
        add_to_favorites: "Thêm Vào Yêu Thích",
        remove_from_favorites: "Xóa Khỏi Yêu Thích",
        no_favorites: "Chưa Có Địa Điểm Yêu Thích",
        
        // About Us Page
        about_us_title: "Về Chúng Tôi",
        about_us_subtitle: "Chúng tôi là nhóm 6 sinh viên đam mê công nghệ và du lịch, cùng nhau xây dựng ứng dụng Vietnam UrbanQuest để khám phá vẻ đẹp Việt Nam",
        developing_team: "Đội Ngũ Phát Triển",
        team_description: "6 thành viên với vai trò và đóng góp khác nhau cho dự án",
        team_leader: "Trưởng Nhóm & Quản Lý Dự Án",
        team_leader_desc: "Chịu trách nhiệm quản lý dự án, thiết kế kiến trúc hệ thống và quản lý dự án với Github",
        frontend_dev: "Lập Trình Viên Frontend",
        frontend_dev_desc: "Phát triển giao diện người dùng, thiết kế UI/UX và tích hợp các tính năng frontend",
        ai_engineer: "Kỹ Sư AI/ML và Backend",
        ai_engineer_desc: "Phát triển hệ thống nhận diện địa điểm dựa trên AI và xây dựng thuật toán gợi ý thông minh",
        database_admin: "Quản Trị Cơ Sở Dữ Liệu",
        database_admin_desc: "Thiết kế cơ sở dữ liệu, quản lý dữ liệu người dùng và tối ưu hóa truy vấn",
        ui_designer: "Thiết Kế UI/UX",
        ui_designer_desc: "Thiết kế giao diện người dùng, tạo wireframe và đảm bảo trải nghiệm người dùng tốt nhất",
        content_manager: "Quản Lý Nội Dung & Kiểm Thử",
        content_manager_desc: "Quản lý nội dung, thu thập dữ liệu địa điểm và kiểm tra chất lượng ứng dụng",
        mission: "Sứ Mệnh",
        mission_desc: "Chúng tôi hướng tới việc tạo ra một công cụ hữu ích giúp du khách và người dân Việt Nam khám phá, ghi lại và chia sẻ vẻ đẹp của những địa danh độc đáo của đất nước. Thông qua công nghệ AI và machine learning, chúng tôi hy vọng mang đến trải nghiệm du lịch thông minh và cá nhân hóa.",
        vision: "Tầm Nhìn",
        vision_desc: "Trở thành nền tảng du lịch thông minh hàng đầu tại Việt Nam, kết nối hàng triệu người yêu thích khám phá. Chúng tôi hy vọng đóng góp vào việc quảng bá văn hóa, lịch sử và những địa điểm đẹp của Việt Nam đến bạn bè quốc tế, đồng thời thúc đẩy du lịch bền vững và có trách nhiệm.",
        core_values: "Giá Trị Cốt Lõi",
        passion: "Đam Mê",
        passion_desc: "Yêu công nghệ và du lịch",
        creativity: "Sáng Tạo",
        creativity_desc: "Luôn đổi mới và cải tiến",
        teamwork: "Làm Việc Nhóm",
        teamwork_desc: "Hợp tác và hỗ trợ lẫn nhau",
        quality: "Chất Lượng",
        quality_desc: "Cam kết chất lượng cao nhất",
        
        // Information Page
        project_info_title: "Thông Tin Dự Án",
        project_info_subtitle: "Vietnam UrbanQuest - Khám Phá Việt Nam Bằng Công Nghệ AI",
        project_overview: "Tổng Quan Dự Án",
        about_project: "Về dự án của chúng tôi",
        about_project_desc1: "Vietnam UrbanQuest là một ứng dụng web du lịch thông minh được phát triển bởi nhóm 6 sinh viên, nhằm giúp người dùng khám phá và trải nghiệm các địa danh nổi tiếng tại Việt Nam một cách dễ dàng và thú vị hơn.",
        about_project_desc2: "Ứng dụng tích hợp công nghệ AI để nhận diện địa danh từ hình ảnh, cung cấp thông tin chi tiết và gợi ý các điểm du lịch phù hợp với sở thích của từng người dùng.",
        target: "Mục Tiêu",
        target1: "Tạo ra công cụ hỗ trợ du lịch thông minh và dễ sử dụng",
        target2: "Ứng dụng công nghệ AI trong nhận diện địa danh",
        target3: "Quảng bá văn hóa và du lịch Việt Nam",
        target4: "Mang đến trải nghiệm cá nhân hóa cho người dùng",
        target5: "Xây dựng cộng đồng người yêu du lịch Việt Nam",
        main_features: "Tính Năng Chính",
        feature_recognition: "Nhận Diện Địa Danh",
        feature_recognition_desc: "Sử dụng AI để nhận diện địa danh từ hình ảnh do người dùng tải lên, cung cấp thông tin cụ thể về địa điểm",
        feature_recommendation: "Gợi Ý Thông Minh",
        feature_recommendation_desc: "Đề xuất điểm du lịch dựa trên sở thích người dùng và các tương tác trước đó",
        feature_album: "Quản Lý Album",
        feature_album_desc: "Lưu trữ và tổ chức ảnh du lịch theo địa điểm và thời gian",
        feature_map: "Bản Đồ Tương Tác",
        feature_map_desc: "Khám phá địa danh và điểm du lịch trên giao diện bản đồ tương tác",
        tech_stack: "Công Nghệ Triển Khai",
        frontend: "Frontend",
        backend: "Backend",
        ai_database: "AI và Cơ Sở Dữ Liệu",
        machine_learning: "Học Máy",
        computer_vision: "Thị Giác Máy Tính",
        json_database: "Cơ Sở Dữ Liệu JSON",
        jwt_auth: "Xác Thực JWT",
        project_stats: "Thống Kê Dự Án",
        landmarks: "Địa Danh",
        members: "Thành Viên",
        lines_code: "Dòng Code",
        development_time: "Thời Gian Phát Triển",

        // Contact
        contact: "Liên hệ",
        
        // Scan Page
        scan_page_title: "Nhận Diện Hình Ảnh",
        scan_page_subtitle: "Tải ảnh lên để nhận diện địa danh và khám phá thông tin",
        upload_pictures: "Tải Ảnh Lên",
        drag_drop: "Kéo và thả tệp vào đây",
        file_limit: "Giới hạn 10MB mỗi tệp - Hỗ trợ JPG, PNG, GIF, WebP",
        browse_files: "Duyệt tệp",
        clear: "Xóa",
        analyze_image: "Phân Tích Ảnh",
        analyzing: "Đang phân tích ảnh của bạn...",
        analyzing_wait: "Điều này có thể mất vài phút",
        recognition_results: "Kết Quả Nhận Diện",
        location_info: "Thông Tin Vị Trí",
        detected_location: "Vị Trí Phát Hiện",
        coordinates: "Tọa Độ",
        address: "Địa Chỉ",
        landmarks: "Địa Danh",
        ai_description: "Mô Tả AI",
        get_nearby_recommendations: "Nhận Gợi Ý Gần Đây",
        add_to_album: "Thêm Vào Album",
        share_results: "Chia Sẻ Kết Quả",
        recognition_failed: "Nhận Diện Thất Bại",
        try_again: "Thử Lại",
        tips_better_recognition: "Mẹo Để Nhận Diện Tốt Hơn",
        photo_quality: "Chất Lượng Ảnh",
        use_high_resolution: "Sử dụng ảnh độ phân giải cao",
        ensure_good_lighting: "Đảm bảo ánh sáng tốt",
        avoid_blurry: "Tránh ảnh mờ hoặc tối",
        include_clear_view: "Bao gồm góc nhìn rõ ràng của địa danh",
        best_results: "Kết Quả Tốt Nhất",
        photos_with_gps: "Ảnh có metadata GPS",
        famous_landmarks: "Địa danh và di tích nổi tiếng",
        tourist_attractions: "Điểm du lịch",
        cultural_sites: "Địa điểm văn hóa và lịch sử",
        
        // Recommendation Page
        rec_page_title: "Gợi Ý Du Lịch",
        rec_page_subtitle: "Khám phá điểm đến tuyệt vời dựa trên sở thích của bạn",
        rec_search_title: "GỢI Ý ĐIỂM ĐẾN DU LỊCH DỰA TRÊN SỞ THÍCH CỦA BẠN",
        rec_search_desc: "Nhập sở thích của bạn để nhận đề xuất du lịch cá nhân hóa",
        rec_interests_placeholder: "Nhập sở thích của bạn (vd: bãi biển, văn hóa, ẩm thực, phiêu lưu)...",
        find_nearby: "Tìm điểm đến gần đây",
        choose_district: "Chọn Quận:",
        select_area: "--Chọn Khu Vực--",
        search_radius: "Bán Kính Tìm Kiếm:",
        current_location: "Vị trí hiện tại",
        quick_suggestions: "Gợi ý nhanh:",
        culture: "Văn Hóa",
        food: "Ẩm Thực",
        adventure: "Phiêu Lưu",
        history: "Lịch Sử",
        nature: "Thiên Nhiên",
        finding_destinations: "Đang tìm điểm đến hoàn hảo cho bạn...",
        popular_destinations: "Điểm Đến Phổ Biến",
        no_destinations_found: "Không tìm thấy điểm đến",
        adjust_search: "Thử điều chỉnh tiêu chí tìm kiếm hoặc duyệt các điểm đến phổ biến của chúng tôi ở trên.",
        location: "Vị Trí",
        rating: "Đánh Giá",
        price: "Giá",
        tags: "Thẻ",
        description: "Mô Tả",
        photo_gallery: "Thư Viện Ảnh",
        
        // Profile Page
        profile_page_title: "Hồ Sơ",
        edit_profile: "Chỉnh Sửa Hồ Sơ",
        statistics: "Thống Kê",
        reviews: "Đánh Giá",
        images: "Hình Ảnh",
        my_reviews: "Đánh Giá Của Tôi",
        bio: "Giới Thiệu",
        save_changes: "Lưu Thay Đổi",
        no_description: "Chưa có mô tả",
        
        // Settings Page
        settings_page_title: "Cài Đặt",
        email_notifications: "Thông Báo Email",
        email_notifications_desc: "Nhận email về cập nhật và gợi ý mới",
        theme_settings: "Giao Diện",
        account: "Tài Khoản",
        delete_account: "Xóa Tài Khoản",
        save_settings: "Lưu Cài Đặt",
        
        // Chatbot Page
        chatbot_page_title: "Trợ Lý Du Lịch AI",
        chatbot_subtitle: "Nhận gợi ý và thông tin du lịch thông minh",
        suggestions: "Gợi Ý",
        clear_history: "Xóa Lịch Sử",
        type_your_message: "Nhập tin nhắn của bạn...",
        send: "Gửi",
        
        // Favorites Page
        favorites_page_title: "Điểm Đến Yêu Thích",
        favorites_page_subtitle: "Danh sách các điểm đến bạn đã lưu",
        no_favorites_yet: "Chưa có điểm đến yêu thích",
        explore_add: "Khám phá và thêm các điểm đến bạn thích!",
        explore_now: "Khám Phá Ngay",
        details: "Chi Tiết",
        
        // Destination Details Page
        dest_back: "Quay Lại",
        loading_info: "Đang tải thông tin...",
        dest_not_found: "Không tìm thấy thông tin điểm đến",
        introduction: "Giới Thiệu",
        province_city: "Tỉnh/Thành Phố",
        distance: "Khoảng Cách",
        share: "Chia Sẻ",
        
        // Login Page
        login_page_title: "Đăng Nhập",
        welcome_back: "Chào mừng trở lại",
        email_label: "Email",
        password_label: "Mật Khẩu",
        or: "Hoặc",
        login_with_google: "Google",
        login_with_facebook: "Facebook",
        dont_have_account: "Chưa có tài khoản?",
        signup_now: "Đăng ký ngay",
        back_to_home: "Quay Lại Trang Chủ",
        
        // Signup Page
        signup_page_title: "Đăng Ký",
        create_account: "Tạo tài khoản mới của bạn",
        full_name_label: "Họ Và Tên",
        phone_label: "Số Điện Thoại",
        confirm_password_label: "Xác Nhận Mật Khẩu",
        terms_agree: "Tôi đồng ý với",
        terms_service: "Điều Khoản Dịch Vụ",
        and: "và",
        privacy_policy: "Chính Sách Bảo Mật",
        already_have_account: "Đã có tài khoản?",
        login_here: "Đăng nhập tại đây",
        
        // Social Page
        social_page_title: "Mạng Xã Hội",
        share_moments: "Chia Sẻ Khoảnh Khắc Du Lịch",
        whats_on_mind: "Bạn đang nghĩ gì về chuyến du lịch của mình?",
        location_optional: "Vị trí (tùy chọn)",
        add_photo: "Thêm Ảnh",
        remove: "Xóa",
        post: "Đăng",
        load_more_posts: "Tải Thêm Bài Viết",
        share_memories: "Chia sẻ kỷ niệm du lịch của bạn với cộng đồng",
        
        // User Menu (reconfirm)
        hello: "Xin chào!",
    },
    
    en: {
        // Navigation
        home: "Home",
        about: "About",
        information: "Information",
        scan: "Scan",
        recommendation: "Recommendations",
        favorites: "Favorites",
        album: "Album",
        chatbot: "Chatbot",
        profile: "Profile",
        settings: "Settings",
        logout: "Logout",
        login: "Login",
        signup: "Sign Up",
        
        // Common
        language: "Language",
        search: "Search",
        cancel: "Cancel",
        save: "Save",
        delete: "Delete",
        edit: "Edit",
        create: "Create",
        upload: "Upload",
        download: "Download",
        close: "Close",
        submit: "Submit",
        back: "Back",
        next: "Next",
        loading: "Loading...",
        
        // Home Page
        discover_hcmc: "Discover Ho Chi Minh City",
        welcome_message: "Welcome to Smart Travel App",
        explore_destinations: "Explore Destinations",
        popular_places: "Popular Places",
        featured_destinations: "Featured Destinations",
        
        // Scan Page
        scan_landmark: "Scan Landmark",
        upload_image: "Upload Image",
        take_photo: "Take Photo",
        recognize: "Recognize",
        recognition_result: "Recognition Result",
        confidence: "Confidence",
        landmark_name: "Landmark Name",
        
        // Recommendation
        get_recommendations: "Get Recommendations",
        your_interests: "Your Interests",
        nearby_places: "Nearby Places",
        ai_recommendations: "AI Recommendations",
        search_by_interest: "Search By Interest",
        search_by_location: "Search By Location",
        
        // Album
        my_albums: "My Albums",
        create_album: "Create Album",
        album_name: "Album Name",
        add_images: "Add Images",
        view_album: "View Album",
        delete_album: "Delete Album",
        download_zip: "Download ZIP",
        all_images: "All Images",
        group_by_landmark: "Group By Landmark",
        photo_albums: "Photo Albums",
        create_album: "Create New Album",
        
        // Profile
        my_profile: "My Profile",
        fullname: "Full Name",
        email: "Email",
        phone: "Phone Number",
        update_profile: "Update Profile",
        change_password: "Change Password",
        
        // Settings
        app_settings: "App Settings",
        notifications: "Notifications",
        theme: "Theme",
        light_theme: "Light",
        dark_theme: "Dark",
        
        // Authentication
        email_address: "Email Address",
        password: "Password",
        confirm_password: "Confirm Password",
        remember_me: "Remember Me",
        forgot_password: "Forgot Password?",
        no_account: "Don't Have An Account?",
        have_account: "Already Have An Account?",
        
        // Forgot Password
        forgot_password_title: "Reset Password",
        forgot_password_instruction: "Enter your email address and we'll send you a reset code.",
        reset_code: "Reset Code",
        new_password: "New Password",
        confirm_new_password: "Confirm New Password",
        send_reset_code: "Send Reset Code",
        reset_password_btn: "Reset Password",
        back_to_login: "Back to Login",
        email: "Email",
        
        // Messages
        success: "Success",
        error: "Error",
        warning: "Warning",
        please_wait: "Please Wait...",
        no_results: "No Results",
        
        // Chatbot
        chatbot_title: "Travel Assistant AI",
        type_message: "Type a Message...",
        send_message: "Send",
        clear_chat: "Clear History",
        
        // Favorites
        my_favorites: "My Favorites",
        add_to_favorites: "Add To Favorites",
        remove_from_favorites: "Remove From Favorites",
        no_favorites: "No Favorite Places Yet",
        
        // About Us Page
        about_us_title: "About Us",
        about_us_subtitle: "We are a group of 6 students passionate about technology and travel, together building the Vietnam UrbanQuest application to explore the beauty of Vietnam",
        developing_team: "Developing Team",
        team_description: "6 members with different roles and contributions to the project",
        team_leader: "Team Leader & Project Manager",
        team_leader_desc: "Responsible for project management, system architecture design and manage project with Github",
        frontend_dev: "Frontend Developer",
        frontend_dev_desc: "User interface development, UI/UX design and frontend feature integration",
        ai_engineer: "AI/ML Engineer and Backend Developing",
        ai_engineer_desc: "Developing an AI-based location recognition system and building a smart suggestion algorithm",
        database_admin: "Database Administrator",
        database_admin_desc: "Database design, user data management, and query optimization",
        ui_designer: "UI/UX Designer",
        ui_designer_desc: "Design user interfaces, create wireframes and ensure the best user experience",
        content_manager: "Content Manager & Tester",
        content_manager_desc: "Content management, location data collection and application quality testing",
        mission: "Mission",
        mission_desc: "We aim to create a useful tool to help tourists and people of Vietnam discover, record and share the beauty of the country's unique landmarks. Through AI and machine learning technology, we hope to bring a smart and personalized travel experience.",
        vision: "Vision",
        vision_desc: "Become the leading smart travel platform in Vietnam, connecting millions of people who love to explore. We hope to contribute to promoting the culture, history and beautiful places of Vietnam to international friends, while promoting sustainable and responsible tourism.",
        core_values: "Core Values",
        passion: "Passion",
        passion_desc: "Love technology and travel",
        creativity: "Creativity",
        creativity_desc: "Always innovate and improve",
        teamwork: "Teamwork",
        teamwork_desc: "Collaborate and support each other",
        quality: "Quality",
        quality_desc: "Commitment to highest quality",
        
        // Information Page
        project_info_title: "Project Information",
        project_info_subtitle: "Vietnam UrbanQuest - Discover VietNam with AI Technology",
        project_overview: "Project Overview",
        about_project: "About our project",
        about_project_desc1: "Vietnam UrbanQuest is a smart travel web application developed by a group of 6 students, to help users explore and experience famous landmarks in Vietnam more easily and interestingly.",
        about_project_desc2: "The application integrates AI technology to recognize landmarks from images, provide detailed information, and recommend tourist destinations that suit each user's interests.",
        target: "Target",
        target1: "Create smart and easy-to-use travel support tools",
        target2: "Application of AI technology in place name recognition",
        target3: "Promote Vietnamese culture and tourism",
        target4: "Provide personalized experiences to users",
        target5: "Build a community of people who love Vietnamese tourism",
        main_features: "Main features",
        feature_recognition: "Landmarks Recognition",
        feature_recognition_desc: "User AI to identify landmarks from images uploaded by users, provide specific information about the location",
        feature_recommendation: "Smart Recommendation",
        feature_recommendation_desc: "Suggest tourist destinations based on user preferrences and previous interactions",
        feature_album: "Album Managing",
        feature_album_desc: "Store and organize your travel photos by location and time",
        feature_map: "Interactive Map",
        feature_map_desc: "Explore landmarks and tourists destinations on an interative map interface",
        tech_stack: "Implemented Technology",
        frontend: "Frontend",
        backend: "Backend",
        ai_database: "AI and Database",
        machine_learning: "Machine Learning",
        computer_vision: "Computer Vision",
        json_database: "JSON Database",
        jwt_auth: "JWT Authentication",
        project_stats: "Project Statistics",
        landmarks: "Landmarks",
        members: "Members",
        lines_code: "Line code",
        development_time: "Development Time",

        // Contact
        contact: "Contact us",
        
        // Scan Page
        scan_page_title: "Image Recognition",
        scan_page_subtitle: "Upload photos to identify landmarks and discover information",
        upload_pictures: "Upload Pictures",
        drag_drop: "Drag and drop files here",
        file_limit: "Limit 10MB per file - Supports JPG, PNG, GIF, WebP",
        browse_files: "Browse files",
        clear: "Clear",
        analyze_image: "Analyze Image",
        analyzing: "Analyzing your image...",
        analyzing_wait: "This may take a few moments",
        recognition_results: "Recognition Results",
        location_info: "Location Information",
        detected_location: "Detected Location",
        coordinates: "Coordinates",
        address: "Address",
        landmarks: "Landmarks",
        ai_description: "AI Description",
        get_nearby_recommendations: "Get Nearby Recommendations",
        add_to_album: "Add to Album",
        share_results: "Share Results",
        recognition_failed: "Recognition Failed",
        try_again: "Try Again",
        tips_better_recognition: "Tips for Better Recognition",
        photo_quality: "Photo Quality",
        use_high_resolution: "Use high-resolution images",
        ensure_good_lighting: "Ensure good lighting",
        avoid_blurry: "Avoid blurry or dark photos",
        include_clear_view: "Include clear view of landmarks",
        best_results: "Best Results",
        photos_with_gps: "Photos with GPS metadata",
        famous_landmarks: "Famous landmarks and monuments",
        tourist_attractions: "Tourist attractions",
        cultural_sites: "Cultural and historical sites",
        
        // Recommendation Page
        rec_page_title: "Travel Recommendations",
        rec_page_subtitle: "Discover amazing destinations based on your interests",
        rec_search_title: "RECOMMEND TRAVEL DESTINATIONS BASED ON YOUR INTERESTS",
        rec_search_desc: "Enter your interests to receive personalized travel suggestions",
        rec_interests_placeholder: "Enter your interests (e.g., beach, culture, food, adventure)...",
        find_nearby: "Find nearby destinations",
        choose_district: "Choose District:",
        select_area: "--Select Area--",
        search_radius: "Search Radius:",
        current_location: "Current location",
        quick_suggestions: "Quick suggestions:",
        culture: "Culture",
        food: "Food",
        adventure: "Adventure",
        history: "History",
        nature: "Nature",
        finding_destinations: "Finding perfect destinations for you...",
        popular_destinations: "Popular Destinations",
        no_destinations_found: "No destinations found",
        adjust_search: "Try adjusting your search criteria or browse our popular destinations above.",
        location: "Location",
        rating: "Rating",
        price: "Price",
        tags: "Tags",
        description: "Description",
        photo_gallery: "Photo Gallery",
        
        // Profile Page
        profile_page_title: "Profile",
        edit_profile: "Edit Profile",
        statistics: "Statistics",
        reviews: "Reviews",
        images: "Images",
        my_reviews: "My Reviews",
        bio: "Bio",
        save_changes: "Save Changes",
        no_description: "No description available",
        
        // Settings Page
        settings_page_title: "Settings",
        email_notifications: "Email Notifications",
        email_notifications_desc: "Receive emails about updates and new recommendations",
        theme_settings: "Theme",
        account: "Account",
        delete_account: "Delete Account",
        save_settings: "Save Settings",
        
        // Chatbot Page
        chatbot_page_title: "Travel Assistant AI",
        chatbot_subtitle: "Get smart travel suggestions and information",
        suggestions: "Suggestions",
        clear_history: "Clear History",
        type_your_message: "Type your message...",
        send: "Send",
        
        // Favorites Page
        favorites_page_title: "Favorite Destinations",
        favorites_page_subtitle: "List of destinations you saved",
        no_favorites_yet: "No favorite destinations yet",
        explore_add: "Explore and add destinations you like!",
        explore_now: "Explore Now",
        details: "Details",
        
        // Destination Details Page
        dest_back: "Back",
        loading_info: "Loading information...",
        dest_not_found: "Destination information not found",
        introduction: "Introduction",
        province_city: "Province/City",
        distance: "Distance",
        share: "Share",
        
        // Login Page
        login_page_title: "Login",
        welcome_back: "Welcome back",
        email_label: "Email",
        password_label: "Password",
        or: "Or",
        login_with_google: "Google",
        login_with_facebook: "Facebook",
        dont_have_account: "Don't Have An Account?",
        signup_now: "Sign up now",
        back_to_home: "Back to Home",
        
        // Signup Page
        signup_page_title: "Sign Up",
        create_account: "Create your new account",
        full_name_label: "Full Name",
        phone_label: "Phone Number",
        confirm_password_label: "Confirm Password",
        terms_agree: "I agree to the",
        terms_service: "Terms of Service",
        and: "and",
        privacy_policy: "Privacy Policy",
        already_have_account: "Already Have An Account?",
        login_here: "Log in here",
        
        // Social Page
        social_page_title: "Social",
        share_moments: "Share Your Travel Moments",
        whats_on_mind: "What's on your mind about your travel?",
        location_optional: "Location (optional)",
        add_photo: "Add Photo",
        remove: "Remove",
        post: "Post",
        load_more_posts: "Load More Posts",
        share_memories: "Share your travel memories with the community",
        
        // User Menu (reconfirm)
        hello: "Hello!",
    }
};

// Language Manager
class LanguageManager {
    constructor() {
        // Default language is English
        this.currentLang = localStorage.getItem('appLanguage') || 'en';
        this.translations = translations;
    }
    
    // Get current language
    getCurrentLanguage() {
        return this.currentLang;
    }
    
    // Set language
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('appLanguage', lang);
            this.updatePageContent();
            return true;
        }
        return false;
    }
    
    // Get translation
    t(key) {
        return this.translations[this.currentLang][key] || key;
    }
    
    // Update all elements with data-i18n attribute
    updatePageContent() {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.placeholder !== undefined) {
                    element.placeholder = translation;
                }
            } else {
                element.textContent = translation;
            }
        });
        
        // Update select options
        document.querySelectorAll('[data-i18n-value]').forEach(element => {
            const key = element.getAttribute('data-i18n-value');
            element.textContent = this.t(key);
        });
    }
    
    // Initialize language switcher
    initLanguageSwitcher(selectElement) {
        if (!selectElement) return;
        
        selectElement.value = this.currentLang;
        selectElement.addEventListener('change', (e) => {
            this.setLanguage(e.target.value);
        });
    }
}

// Create global instance
const langManager = new LanguageManager();

// Auto-initialize on page load
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        // Update page content
        langManager.updatePageContent();
        
        // Initialize all language selectors
        document.querySelectorAll('.language-selector').forEach(selector => {
            langManager.initLanguageSwitcher(selector);
        });
    });
}
