using System;
using System.Threading.Tasks;
using Microsoft.JSInterop;

namespace HealthcareChatbot.Services
{
    public class ThemeService
    {
        private readonly IJSRuntime _jsRuntime;
        private bool _isDarkMode;
        
        public bool IsDarkMode
        {
            get => _isDarkMode;
            set
            {
                if (_isDarkMode != value)
                {
                    _isDarkMode = value;
                    OnChange?.Invoke();
                    _jsRuntime.InvokeVoidAsync("applyTheme", _isDarkMode);
                }
            }
        }

        public event Action OnChange;

        public ThemeService(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime;
            InitializeTheme();
        }

        private async void InitializeTheme()
        {
            await _jsRuntime.InvokeVoidAsync("initializeTheme");
        }

        private async void SaveThemePreference()
        {
            try
            {
                await _jsRuntime.InvokeVoidAsync("localStorage.setItem", "theme", _isDarkMode ? "dark" : "light");
                await ApplyTheme();
            }
            catch
            {
                // Ignore errors when saving preference
            }
        }

        private async Task ApplyTheme()
        {
            try
            {
                await _jsRuntime.InvokeVoidAsync("applyTheme", _isDarkMode);
            }
            catch
            {
                // Ignore errors when applying theme
            }
        }

        public async Task ToggleDarkMode()
        {
            IsDarkMode = !IsDarkMode;
            await Task.CompletedTask;
        }
    }
} 