using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace HealthcareChatbot.Services;

public class ApiService
{
    private readonly HttpClient _httpClient;
    private const string BaseUrl = "http://localhost:8000";

    public ApiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<string> GetHealthTipsAsync(string query)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync($"{BaseUrl}/health-tips", new { query });
            response.EnsureSuccessStatusCode();
            var result = await response.Content.ReadFromJsonAsync<HealthTipsResponse>();
            return result?.response ?? "Sorry, I couldn't process your request at this time.";
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error getting health tips: {ex.Message}");
            return "Sorry, I couldn't process your request at this time.";
        }
    }

    public async Task<List<string>> GetSampleQueriesAsync()
    {
        try
        {
            // Try to get sample queries from the backend
            var response = await _httpClient.PostAsync($"{BaseUrl}/generate-sample-queries", null);
            
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                try
                {
                    // Try to parse as SampleQueriesResponse
                    var result = JsonSerializer.Deserialize<SampleQueriesResponse>(content);
                    return result?.queries ?? GetDefaultQueries();
                }
                catch
                {
                    // If that fails, try to parse as a simple string array
                    try
                    {
                        var queries = JsonSerializer.Deserialize<List<string>>(content);
                        return queries ?? GetDefaultQueries();
                    }
                    catch
                    {
                        // If all parsing fails, return default queries
                        return GetDefaultQueries();
                    }
                }
            }
            
            return GetDefaultQueries();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error getting sample queries: {ex.Message}");
            return GetDefaultQueries();
        }
    }

    public async Task<string> DetectDiseaseAsync(List<string> symptoms)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync($"{BaseUrl}/detect-disease", new { symptoms });
            response.EnsureSuccessStatusCode();
            var result = await response.Content.ReadFromJsonAsync<DiseaseResponse>();
            return result?.response ?? "Sorry, I couldn't analyze your symptoms at this time.";
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error detecting disease: {ex.Message}");
            return "Sorry, I couldn't analyze your symptoms at this time.";
        }
    }

    public async Task<string> GenerateResponseAsync(string query)
    {
        try
        {
            // Create a proper request object that matches what the backend expects
            var request = new { message = query };
            var response = await _httpClient.PostAsJsonAsync($"{BaseUrl}/generate-response", request);
            
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<GenerateResponse>();
                return result?.response ?? "Sorry, I couldn't process your request at this time.";
            }
            else
            {
                // Log the error status code
                Console.WriteLine($"Error generating response: {response.StatusCode}");
                return "Sorry, I couldn't process your request at this time.";
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error generating response: {ex.Message}");
            return "Sorry, I couldn't process your request at this time.";
        }
    }

    private List<string> GetDefaultQueries()
    {
        return new List<string>
        {
            "What are the symptoms of the flu?",
            "How can I manage diabetes?",
            "What are some tips for better sleep?",
            "How to maintain a healthy diet?",
            "What are the signs of depression?"
        };
    }
}

public class HealthTipsResponse
{
    [JsonPropertyName("response")]
    public string response { get; set; }
}

public class DiseaseResponse
{
    [JsonPropertyName("response")]
    public string response { get; set; }
}

public class GenerateResponse
{
    [JsonPropertyName("response")]
    public string response { get; set; }
}

public class SampleQueriesResponse
{
    [JsonPropertyName("queries")]
    public List<string> queries { get; set; }
} 