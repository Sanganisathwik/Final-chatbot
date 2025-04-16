// Theme management functions
window.applyTheme = function (isDarkMode) {
    document.documentElement.classList.toggle('mud-dark-theme', isDarkMode);
    document.body.classList.toggle('dark-theme', isDarkMode);
    
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.setAttribute('content', isDarkMode ? '#121212' : '#ffffff');
    } else {
        const meta = document.createElement('meta');
        meta.name = 'theme-color';
        meta.content = isDarkMode ? '#121212' : '#ffffff';
        document.head.appendChild(meta);
    }
    
    // Dispatch event for other components to react
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { isDarkMode } }));
};

// Initialize theme on page load
window.initializeTheme = function () {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme === 'dark');
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark);
    }
};

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) {
        applyTheme(e.matches);
    }
});

// Call initialize on page load
document.addEventListener('DOMContentLoaded', initializeTheme);