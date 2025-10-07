/**
 * API Client for Toyota Chatbot
 * Centralized API calls - all requests go through Express proxy
 * No direct backend URLs - avoids CORS and localhost issues
 */

import type { Car, Promotion, CarRecommendationData, CarComparisonData } from './types';

// API Base URL - relative path, akan di-proxy oleh Express server
const API_BASE_URL = '/api';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(
	endpoint: string,
	options?: RequestInit
): Promise<T> {
	const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
	
	try {
		const response = await fetch(url, {
			headers: {
				'Content-Type': 'application/json',
				...options?.headers
			},
			...options
		});

		if (!response.ok) {
			throw new Error(`HTTP ${response.status}: ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error(`API Error [${endpoint}]:`, error);
		throw error;
	}
}

/**
 * Chat API - Send message to assistant
 */
export async function sendChatMessage(
	message: string,
	sessionId?: string
): Promise<{ 'session-id': string | null; output: string }> {
	return fetchAPI('/chat', {
		method: 'POST',
		body: JSON.stringify({
			message,
			context: sessionId ? { 'session-id': sessionId } : {}
		})
	});
}

/**
 * Get car recommendations based on criteria
 */
export async function getCarRecommendations(params: {
	budget_min?: number;
	budget_max?: number;
	segment?: string;
	fuel_type?: string;
	seating?: number;
	use_case?: string;
	limit?: number;
}): Promise<{ data: Car[]; total: number; generation_info?: any }> {
	const queryParams = new URLSearchParams();
	
	Object.entries(params).forEach(([key, value]) => {
		if (value !== undefined && value !== null) {
			queryParams.append(key, String(value));
		}
	});

	const endpoint = `/recommendations${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
	return fetchAPI(endpoint);
}

/**
 * Compare multiple car variants
 */
export async function compareVariants(
	variantIds: string[]
): Promise<{ data: Car[]; comparison_summary: any }> {
	const queryParams = new URLSearchParams();
	variantIds.forEach(id => queryParams.append('variant_ids', id));

	const endpoint = `/compare?${queryParams.toString()}`;
	return fetchAPI(endpoint);
}

/**
 * Get variant details by ID
 */
export async function getVariantDetails(
	variantId: string
): Promise<{ data: Car }> {
	return fetchAPI(`/variants/${variantId}`);
}

/**
 * Get active promotions
 */
export async function getPromotions(params?: {
	active_only?: boolean;
	variant_id?: string;
}): Promise<{ data: Promotion[]; total: number }> {
	const queryParams = new URLSearchParams();
	
	if (params?.active_only !== undefined) {
		queryParams.append('active_only', String(params.active_only));
	}
	if (params?.variant_id) {
		queryParams.append('variant_id', params.variant_id);
	}

	const endpoint = `/promotions${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
	return fetchAPI(endpoint);
}

/**
 * Get stock availability
 */
export async function getStockAvailability(params: {
	variant_id?: string;
	city?: string;
}): Promise<{ data: any[] }> {
	const queryParams = new URLSearchParams();
	
	Object.entries(params).forEach(([key, value]) => {
		if (value) queryParams.append(key, value);
	});

	const endpoint = `/stock${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
	return fetchAPI(endpoint);
}

/**
 * Get all cars
 */
export async function getAllCars(params?: {
	segment?: string;
	limit?: number;
	offset?: number;
}): Promise<{ data: any[]; total: number }> {
	const queryParams = new URLSearchParams();
	
	if (params) {
		Object.entries(params).forEach(([key, value]) => {
			if (value !== undefined) queryParams.append(key, String(value));
		});
	}

	const endpoint = `/cars${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
	return fetchAPI(endpoint);
}

/**
 * Get accessories
 */
export async function getAccessories(): Promise<{ data: any[] }> {
	return fetchAPI('/accessories');
}

/**
 * Get workshops
 */
export async function getWorkshops(city?: string): Promise<{ data: any[] }> {
	const endpoint = city ? `/workshops?city=${city}` : '/workshops';
	return fetchAPI(endpoint);
}

/**
 * Get communities
 */
export async function getCommunities(params?: {
	city?: string;
	focus_model?: string;
}): Promise<{ data: any[] }> {
	const queryParams = new URLSearchParams();
	
	if (params?.city) queryParams.append('city', params.city);
	if (params?.focus_model) queryParams.append('focus_model', params.focus_model);

	const endpoint = `/communities${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
	return fetchAPI(endpoint);
}

/**
 * Parse structured response from chat
 * Detects if response contains structured data (recommendations, comparison, etc)
 */
export function parseStructuredResponse(output: string | any): {
	type: 'text' | 'car_recommendation' | 'car_comparison' | 'car_info' | 'promotion';
	data: any;
} {
	// If output is already structured
	if (typeof output === 'object' && output !== null) {
		if ('type' in output && 'data' in output) {
			return output;
		}
	}

	// If output is string, try to parse as JSON
	if (typeof output === 'string') {
		try {
			const parsed = JSON.parse(output);
			if (parsed.type && parsed.data) {
				return parsed;
			}
		} catch {
			// Not JSON, return as text
		}
	}

	// Default to text type
	return {
		type: 'text',
		data: typeof output === 'string' ? output : JSON.stringify(output)
	};
}

/**
 * Build query params helper
 */
export function buildQueryParams(params: Record<string, any>): string {
	const query = new URLSearchParams();
	
	Object.entries(params).forEach(([key, value]) => {
		if (value !== undefined && value !== null && value !== '') {
			if (Array.isArray(value)) {
				value.forEach(v => query.append(key, String(v)));
			} else {
				query.append(key, String(value));
			}
		}
	});

	const queryString = query.toString();
	return queryString ? `?${queryString}` : '';
}

// Export types for convenience
export type { Car, Promotion, CarRecommendationData, CarComparisonData };
