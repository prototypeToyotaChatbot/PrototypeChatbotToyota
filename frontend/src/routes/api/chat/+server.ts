import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

const GATEWAY_URL = env.GATEWAY_URL ?? 'http://localhost:2323';
const DEFAULT_ERROR_MESSAGE = "I'm experiencing some technical difficulties. Please try again later.";

type ChatEnvelope = {
	'session-id': string | null;
	output: string;
};

const normalizePayload = (
	payload: unknown,
	fallback: ChatEnvelope
): (Record<string, unknown> & ChatEnvelope) => {
	const result: Record<string, unknown> & { session_id?: unknown } = {
		...fallback
	};

	if (payload && typeof payload === 'object') {
		Object.assign(result, payload as Record<string, unknown>);
	}

	if (!('session-id' in result) && 'session_id' in result) {
		result['session-id'] = result.session_id as string | null;
	}

	delete result.session_id;

	if (typeof result.output !== 'string') {
		result.output = String(result.output ?? '');
	}

	return result as Record<string, unknown> & ChatEnvelope;
};

export const POST: RequestHandler = async ({ request }) => {
	let fallbackEnvelope: ChatEnvelope = {
		'session-id': null,
		output: DEFAULT_ERROR_MESSAGE
	};

	try {
		const body = await request.json();
		const context =
			body && typeof body === 'object' && body !== null && typeof body.context === 'object' && body.context !== null
				? body.context
				: {};

		fallbackEnvelope = {
			'session-id': context.session_id ?? null,
			output: DEFAULT_ERROR_MESSAGE
		};

		const response = await fetch(`${GATEWAY_URL}/api/chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});

		let data: unknown = null;
		try {
			data = await response.json();
		} catch {
			data = null;
		}

		if (!response.ok) {
			const errorPayload = normalizePayload(data, fallbackEnvelope);
			if (!errorPayload.output || !errorPayload.output.trim()) {
				errorPayload.output = DEFAULT_ERROR_MESSAGE;
			}
			return json(errorPayload, { status: response.status });
		}

		const successPayload = normalizePayload(data, {
			...fallbackEnvelope,
			output: ''
		});

		return json(successPayload);
	} catch (error) {
		console.error('Chat proxy error:', error);
		return json(fallbackEnvelope, { status: 500 });
	}
};
