import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

const GATEWAY_URL = 'http://prototypechatbot-gateway-1:2323';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const body = await request.json();
		
		const response = await fetch(`${GATEWAY_URL}/api/chat`, {
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
		console.error('Chat proxy error:', error);
		return json(
			{ response: 'I\'m experiencing some technical difficulties. Please try again later.' },
			{ status: 500 }
		);
	}
};