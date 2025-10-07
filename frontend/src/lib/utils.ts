import type { PriceFormat, FormatPriceOptions } from './types';

/**
 * Format price to Indonesian Rupiah
 */
export function formatPrice(
	price: PriceFormat,
	options: FormatPriceOptions = {}
): string {
	const {
		currency = 'IDR',
		locale = 'id-ID',
		minimumFractionDigits = 0,
		maximumFractionDigits = 0
	} = options;

	const numPrice = typeof price === 'string' ? parseFloat(price) : price;

	return new Intl.NumberFormat(locale, {
		style: 'currency',
		currency,
		minimumFractionDigits,
		maximumFractionDigits
	}).format(numPrice);
}

/**
 * Format date to Indonesian locale
 */
export function formatDate(dateStr: string | Date): string {
	try {
		const date = typeof dateStr === 'string' ? new Date(dateStr) : dateStr;
		return date.toLocaleDateString('id-ID', {
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		});
	} catch {
		return typeof dateStr === 'string' ? dateStr : dateStr.toISOString();
	}
}

/**
 * Format time to Indonesian locale
 */
export function formatTime(date: Date): string {
	return date.toLocaleTimeString('id-ID', {
		hour: '2-digit',
		minute: '2-digit'
	});
}

/**
 * Calculate discount percentage
 */
export function calculateDiscount(
	original: PriceFormat,
	discounted: PriceFormat
): number {
	const origPrice = typeof original === 'string' ? parseFloat(original) : original;
	const discPrice = typeof discounted === 'string' ? parseFloat(discounted) : discounted;
	return Math.round(((origPrice - discPrice) / origPrice) * 100);
}

/**
 * Generate unique ID
 */
export function generateId(): string {
	if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
		return crypto.randomUUID();
	}
	return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
	if (text.length <= maxLength) return text;
	return text.slice(0, maxLength - 3) + '...';
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
	func: T,
	wait: number
): (...args: Parameters<T>) => void {
	let timeout: ReturnType<typeof setTimeout> | null = null;
	
	return function executedFunction(...args: Parameters<T>) {
		const later = () => {
			timeout = null;
			func(...args);
		};
		
		if (timeout) clearTimeout(timeout);
		timeout = setTimeout(later, wait);
	};
}

/**
 * Check if element is in viewport
 */
export function isInViewport(element: HTMLElement): boolean {
	const rect = element.getBoundingClientRect();
	return (
		rect.top >= 0 &&
		rect.left >= 0 &&
		rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
		rect.right <= (window.innerWidth || document.documentElement.clientWidth)
	);
}

/**
 * Smooth scroll to element
 */
export function scrollToElement(element: HTMLElement, options: ScrollIntoViewOptions = {}): void {
	element.scrollIntoView({
		behavior: 'smooth',
		block: 'nearest',
		...options
	});
}

/**
 * Get scroll position
 */
export function getScrollPosition(element?: HTMLElement): { x: number; y: number } {
	if (element) {
		return {
			x: element.scrollLeft,
			y: element.scrollTop
		};
	}
	return {
		x: window.pageXOffset || document.documentElement.scrollLeft,
		y: window.pageYOffset || document.documentElement.scrollTop
	};
}

/**
 * Check if device is mobile
 */
export function isMobile(): boolean {
	if (typeof window === 'undefined') return false;
	return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
		navigator.userAgent
	);
}

/**
 * Get device info
 */
export function getDeviceInfo(): {
	isMobile: boolean;
	isTablet: boolean;
	isDesktop: boolean;
	os: string;
} {
	if (typeof window === 'undefined') {
		return { isMobile: false, isTablet: false, isDesktop: true, os: 'unknown' };
	}

	const ua = navigator.userAgent;
	const mobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua);
	const tablet = /iPad|Android/i.test(ua) && !/Mobile/i.test(ua);

	let os = 'unknown';
	if (/Windows/i.test(ua)) os = 'Windows';
	else if (/Mac/i.test(ua)) os = 'macOS';
	else if (/Linux/i.test(ua)) os = 'Linux';
	else if (/Android/i.test(ua)) os = 'Android';
	else if (/iOS|iPhone|iPad|iPod/i.test(ua)) os = 'iOS';

	return {
		isMobile: mobile && !tablet,
		isTablet: tablet,
		isDesktop: !mobile && !tablet,
		os
	};
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
	try {
		if (navigator.clipboard) {
			await navigator.clipboard.writeText(text);
			return true;
		}
		// Fallback for older browsers
		const textArea = document.createElement('textarea');
		textArea.value = text;
		textArea.style.position = 'fixed';
		textArea.style.left = '-999999px';
		document.body.appendChild(textArea);
		textArea.focus();
		textArea.select();
		const successful = document.execCommand('copy');
		document.body.removeChild(textArea);
		return successful;
	} catch (err) {
		console.error('Failed to copy text: ', err);
		return false;
	}
}
