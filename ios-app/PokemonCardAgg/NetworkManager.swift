import Foundation

enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingError
    case serverError(String)
    
    var localizedDescription: String {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .noData:
            return "No data received from server"
        case .decodingError:
            return "Failed to decode response"
        case .serverError(let message):
            return message
        }
    }
}

@MainActor
class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    
    // Base URL for the Flask API
    // For iOS Simulator: use http://127.0.0.1:5000
    // For physical device: use your computer's local IP (e.g., http://192.168.1.100:5000)
    private let baseURL = "http://127.0.0.1:5000"
    
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private init() {}
    
    /// Search for Pokemon cards
    /// - Parameter query: Search query (e.g., "Charizard")
    /// - Returns: SearchResult containing card metadata and listings
    func search(query: String) async throws -> SearchResult {
        guard !query.isEmpty else {
            throw NetworkError.invalidURL
        }
        
        // Construct URL with query parameter
        guard var urlComponents = URLComponents(string: "\(baseURL)/search") else {
            throw NetworkError.invalidURL
        }
        
        urlComponents.queryItems = [
            URLQueryItem(name: "q", value: query)
        ]
        
        guard let url = urlComponents.url else {
            throw NetworkError.invalidURL
        }
        
        isLoading = true
        errorMessage = nil
        
        defer {
            isLoading = false
        }
        
        do {
            // Make the request
            let (data, response) = try await URLSession.shared.data(from: url)
            
            // Check response status
            guard let httpResponse = response as? HTTPURLResponse else {
                throw NetworkError.serverError("Invalid response")
            }
            
            guard httpResponse.statusCode == 200 else {
                // Try to decode error message
                if let errorDict = try? JSONDecoder().decode([String: String].self, from: data),
                   let errorMsg = errorDict["error"] {
                    throw NetworkError.serverError(errorMsg)
                }
                throw NetworkError.serverError("Server returned status code \(httpResponse.statusCode)")
            }
            
            // Decode the response
            let decoder = JSONDecoder()
            let searchResult = try decoder.decode(SearchResult.self, from: data)
            
            return searchResult
            
        } catch let error as NetworkError {
            errorMessage = error.localizedDescription
            throw error
        } catch {
            errorMessage = "Network error: \(error.localizedDescription)"
            throw NetworkError.serverError(error.localizedDescription)
        }
    }
    
    /// Check if the API is healthy
    /// - Returns: True if the API is responding
    func checkHealth() async -> Bool {
        guard let url = URL(string: "\(baseURL)/health") else {
            return false
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return false
            }
            
            if let healthDict = try? JSONDecoder().decode([String: String].self, from: data),
               healthDict["status"] == "healthy" {
                return true
            }
            
            return false
        } catch {
            return false
        }
    }
}
