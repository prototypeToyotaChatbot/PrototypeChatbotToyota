import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

const GATEWAY_URL = env.GATEWAY_URL ?? 'http://localhost:2323';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const body = await request.json();
		
		const response = await fetch(`${GATEWAY_URL}/api/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});

		const data = await response.json();
		
		if (!response.ok) {
			return json(data, { status: response.status });
		}

		return json(data);
	} catch (error) {
		console.error('Login proxy error:', error);
		return json(
			{ message: 'Network error. Please try again.' },
			{ status: 500 }
		);
	}
};