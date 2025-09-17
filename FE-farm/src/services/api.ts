const API_BASE_URL = 'http://127.0.0.1:8000/api';

export interface Medicine {
  id: number;
  name: string;
  packaging?: string;
  price_unit?: number;
  price_total?: number;
  is_published: boolean;
  published_at?: string;
  updated_at?: string;
}

export interface Pig {
  id: number;
  name: string;
  price?: number;
  is_published: boolean;
  published_at?: string;
  updated_at?: string;
}

export interface NewsCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  color?: string;
  icon?: string;
  parent_id?: number;
  sort_order: number;
  is_published: boolean;
  published_at?: string;
  created_at?: string;
  updated_at?: string;
}

export interface NewsArticle {
  id: number;
  title: string;
  slug: string;
  summary?: string;
  content?: string;
  featured_image?: string;
  category_id?: number;  // Note: Not implemented in cms_content_entry yet
  author?: string;
  read_time?: number;
  view_count: number;  // Note: Always 0 for now, not tracked in cms_content_entry
  tags: string[];
  meta_title?: string;
  meta_description?: string;
  is_featured: boolean;  // Note: Always false for now, not implemented in cms_content_entry
  is_published: boolean;
  published_at?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T[];
  pagination?: {
    current_page: number;
    total_pages: number;
    total_items: number;
    page_size: number;
    has_next: boolean;
    has_previous: boolean;
  };
  message?: string;
}

export interface ApiParams {
  page?: number;
  page_size?: number;
  search?: string;
  published?: boolean;
}

export interface NewsApiParams extends ApiParams {
  category?: string;
  featured?: boolean;
}

class ApiService {
  private async request<T>(endpoint: string, params?: ApiParams): Promise<ApiResponse<T>> {
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          url.searchParams.append(key, value.toString());
        }
      });
    }

    try {
      const response = await fetch(url.toString());
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async getMedicines(params?: ApiParams): Promise<ApiResponse<Medicine>> {
    return this.request<Medicine>('/medicines/', params);
  }

  async getPigs(params?: ApiParams): Promise<ApiResponse<Pig>> {
    return this.request<Pig>('/pigs/', params);
  }

  async getPig(pigId: number): Promise<{ status: string; data: Pig; message?: string }> {
    const response = await fetch(`${API_BASE_URL}/pigs/${pigId}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async getMedicine(medicineId: number): Promise<{ status: string; data: Medicine; message?: string }> {
    const response = await fetch(`${API_BASE_URL}/medicines/${medicineId}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async getNewsArticles(params?: NewsApiParams): Promise<ApiResponse<NewsArticle>> {
    return this.request<NewsArticle>('/news/', params);
  }

  async getNewsArticle(articleId: number): Promise<{ status: string; data: NewsArticle; message?: string }> {
    const response = await fetch(`${API_BASE_URL}/news/${articleId}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async getNewsCategories(): Promise<{ status: string; data: NewsCategory[]; message?: string }> {
    const response = await fetch(`${API_BASE_URL}/news/categories/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    const response = await fetch(`${API_BASE_URL}/health/`);
    return response.json();
  }
}

export const apiService = new ApiService();