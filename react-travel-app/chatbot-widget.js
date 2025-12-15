// Chatbot Widget - Include this in all HTML pages
(function() {
    console.log('[Chatbot Widget] Script loaded');
    
    // Create chatbot HTML structure
    function initChatbotWidget() {
        console.log('[Chatbot Widget] Initializing...');
        
        // Check if already initialized
        if (document.getElementById('chatbot-widget-container')) {
            console.log('[Chatbot Widget] Already initialized');
            return;
        }

        // Create container
        const container = document.createElement('div');
        container.id = 'chatbot-widget-container';
        
        // Add chatbot button and modal HTML
        container.innerHTML = `
            <!-- Chatbot Button -->
            <button id="chatbotButton" class="chatbot-button" title="Open Travel Chat Assistant" onclick="toggleChatbotWidget()">
                <i class="fas fa-comments"></i>
            </button>

            <!-- Chatbot Modal -->
            <div id="chatbotModal" class="chatbot-modal">
                <div class="chatbot-header">
                    <h3> 🤖 Smart Travel Assistant</h3>
                    <button id="chatbotCloseBtn" class="chatbot-close-btn" onclick="closeChatbotWidget()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="chatbot-frame">
                    <iframe src="chatbot.html" style="width: 100%; height: 100%; border: none;"></iframe>
                </div>
            </div>
        `;
        
        document.body.appendChild(container);
        
        // Add styles
        addChatbotStyles();
        
        // Add event listeners
        addChatbotEventListeners();
    }

    // Add CSS styles for chatbot
    function addChatbotStyles() {
        if (document.getElementById('chatbot-widget-styles')) {
            return; // Already added
        }

        const style = document.createElement('style');
        style.id = 'chatbot-widget-styles';
        style.textContent = `
            /* Chatbot Styles */
            .chatbot-button {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 28px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                z-index: 99;
            }

            .chatbot-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            .chatbot-button:active {
                transform: scale(0.95);
            }

            .chatbot-modal {
                display: none;
                position: fixed;
                bottom: 100px;
                right: 30px;
                width: 380px;
                height: 400px;
                
                background: white;
                border-radius: 15px;
                box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
                z-index: 98;
                flex-direction: column;
                overflow: hidden;
            }

            .chatbot-modal.active {
                display: flex;
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .chatbot-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-shrink: 0;
            }

            .chatbot-header h3 {
                margin: 0;
                font-size: 18px;
                font-weight: bold;
            }

            .chatbot-close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
            }

            .chatbot-close-btn:hover {
                transform: rotate(90deg);
            }

            .chatbot-frame {
                flex: 1;
                overflow: hidden;
            }

            .chatbot-frame iframe {
                width: 100%;
                height: 100%;
                border: none;
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .chatbot-button {
                    bottom: 20px;
                    right: 20px;
                    width: 50px;
                    height: 50px;
                    font-size: 24px;
                }

                .chatbot-modal {
                    bottom: 80px;
                    right: 20px;
                    width: calc(100% - 40px);
                    max-width: 400px;
                }
            }

            @media (max-width: 480px) {
                .chatbot-modal {
                    width: calc(100vw - 20px);
                    height: calc(100vh - 100px);
                    bottom: 10px;
                    max-height: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Add event listeners for chatbot interactions
    function addChatbotEventListeners() {
        const chatbotButton = document.getElementById('chatbotButton');
        const chatbotModal = document.getElementById('chatbotModal');
        const chatbotCloseBtn = document.getElementById('chatbotCloseBtn');

        if (chatbotButton && chatbotModal && chatbotCloseBtn) {
            // Define global functions
            window.toggleChatbotWidget = function() {
                chatbotModal.classList.toggle('active');
            };

            window.closeChatbotWidget = function() {
                chatbotModal.classList.remove('active');
            };

            // Close modal when clicking outside
            document.addEventListener('click', function(event) {
                if (!chatbotButton.contains(event.target) && 
                    !chatbotModal.contains(event.target)) {
                    chatbotModal.classList.remove('active');
                }
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbotWidget);
    } else {
        initChatbotWidget();
    }
})();
