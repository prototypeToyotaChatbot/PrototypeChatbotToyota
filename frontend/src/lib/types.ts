// Message Types
export type MessageType = 'text' | 'car_recommendation' | 'car_comparison' | 'promotion' | 'car_info';

export interface Message {
	id: number;
	text: string;
	isUser: boolean;
	timestamp: Date;
	data?: MessageData;
	type?: MessageType;
}

// Car Types
export interface CarSpecs {
	engine?: string;
	transmission?: string;
	fuel_type?: string;
	seating_capacity?: number;
}

export interface CarFeatures {
	safety?: string[];
	comfort?: string[];
}

export interface Car {
	name: string;
	variant?: string;
	price: string | number;
	image_url?: string;
	catalog_link?: string;
	specs?: CarSpecs;
	features?: string[] | CarFeatures;
	benefits?: string[];
	use_cases?: string[];
}

// Generation Info
export interface GenerationInfo {
	generation: string;
	characteristics: string[];
}

// Data Types for Different Message Types
export interface CarRecommendationData {
	type: 'car_recommendation';
	cars?: Car[];
	generation_info?: GenerationInfo;
}

export interface CarComparisonData {
	type: 'car_comparison';
	cars?: Car[];
	comparison_points?: string[];
}

export interface CarInfoData {
	type: 'car_info';
	car?: Car;
}

export interface Promotion {
	title: string;
	discount_amount?: string | number;
	discount_percentage?: string | number;
	variant_name: string;
	model_name: string;
	original_price: string | number;
	discounted_price?: string | number;
	start_date?: string;
	end_date?: string;
	terms?: string;
}

export interface PromotionData {
	type: 'promotion';
	promotions?: Promotion[];
}

export type MessageData = CarRecommendationData | CarComparisonData | CarInfoData | PromotionData;

// API Types
export interface ChatContext {
	session_id?: string;
	'session-id'?: string;
	session_started_at?: string;
	locale?: string;
	timezone?: string;
	[key: string]: any;
}

export interface ChatRequest {
	message: string;
	context?: ChatContext;
}

export interface ChatResponse {
	'session-id': string;
	output: string;
	data?: MessageData;
}

// Utility Types
export type PriceFormat = string | number;

export interface FormatPriceOptions {
	currency?: string;
	locale?: string;
	minimumFractionDigits?: number;
	maximumFractionDigits?: number;
}
