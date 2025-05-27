/**
 * 智能教育对话系统主要JavaScript文件
 */

// 当文档加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 激活当前页面的导航链接
    activateCurrentNavLink();
    
    // 初始化工具提示
    initializeTooltips();
});

/**
 * 激活当前页面对应的导航链接
 */
function activateCurrentNavLink() {
    const currentPath = window.location.pathname;
    
    // 查找所有导航链接
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    // 遍历链接，检查是否匹配当前路径
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // 如果链接的href与当前路径匹配，则添加active类
        if (href === currentPath || 
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
}

/**
 * 初始化Bootstrap工具提示
 */
function initializeTooltips() {
    // 查找所有带有data-bs-toggle="tooltip"属性的元素
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    
    // 初始化工具提示
    if (typeof bootstrap !== 'undefined' && tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise} 表示复制操作是否成功的Promise
 */
function copyToClipboard(text) {
    // 使用现代的剪贴板API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text)
            .then(() => true)
            .catch(() => false);
    }
    
    // 回退方法（不支持剪贴板API的浏览器）
    try {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        return Promise.resolve(true);
    } catch (err) {
        return Promise.resolve(false);
    }
}

/**
 * 显示提示消息
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型：success, warning, danger, info
 * @param {number} duration - 显示时长（毫秒）
 */
function showNotification(message, type = 'info', duration = 3000) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification fade-in`;
    notification.textContent = message;
    
    // 添加到页面
    const container = document.createElement('div');
    container.className = 'notification-container';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    container.appendChild(notification);
    document.body.appendChild(container);
    
    // 设置定时器移除通知
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(container);
        }, 500);
    }, duration);
} 