<script lang="ts">
	import { onMount } from 'svelte';

	const generateId = () =>
		typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function'
			? crypto.randomUUID()
			: `${Date.now()}-${Math.random().toString(16).slice(2)}`;

	let messages: Array<{ id: number; text: string; isUser: boolean; timestamp: Date }> = [];
	let inputMessage = '';
	let isLoading = false;
	let chatContainer: HTMLDivElement;
	let sessionId = generateId();
	let sessionStartedAt = new Date().toISOString();

	onMount(() => {
		if (typeof window !== 'undefined') {
			sessionId = generateId();
			sessionStartedAt = new Date().toISOString();
		}

		messages = [
			{
				id: Date.now(),
				text: "Hello! I'm your chatbot assistant. How can I help you today?",
				isUser: false,
				timestamp: new Date()
			}
		];
	});

	async function sendMessage() {
		if (!inputMessage.trim() || isLoading) return;

		const userMessage = inputMessage.trim();
		inputMessage = '';

		messages = [
			...messages,
			{
				id: Date.now(),
				text: userMessage,
				isUser: true,
				timestamp: new Date()
			}
		];

		isLoading = true;

		try {
			const context = {
				session_id: sessionId,
				session_started_at: sessionStartedAt,
				locale: typeof navigator !== 'undefined' ? navigator.language : undefined,
				timezone:
					typeof Intl !== 'undefined'
						? Intl.DateTimeFormat().resolvedOptions().timeZone
						: undefined
			};

			const response = await fetch('/api/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					message: userMessage,
					context
				})
			});

			let botResponse = '';
			let payload: any = null;
			try {
				payload = await response.json();
			} catch (parseError) {
				payload = null;
			}

			const returnedSessionId = payload?.['session-id'] ?? payload?.session_id;
			if (returnedSessionId) {
				sessionId = returnedSessionId;
			}

			const extractOutput = (data: any) => {
				const outputValue = typeof data?.output === 'string' ? data.output : undefined;
				return outputValue && outputValue.trim().length > 0 ? outputValue : undefined;
			};

			if (response.ok && payload) {
				botResponse = extractOutput(payload) ?? 'I received your message: ' + userMessage;
			} else {
				botResponse = extractOutput(payload) ?? "Sorry, I'm having trouble connecting right now. Please try again later.";
			}

			messages = [
				...messages,
				{
					id: Date.now() + 1,
					text: botResponse,
					isUser: false,
					timestamp: new Date()
				}
			];
		} catch (error) {
			console.error('Error sending message:', error);
			messages = [
				...messages,
				{
					id: Date.now() + 1,
					text: "Sorry, I'm having trouble connecting right now. Please try again later.",
					isUser: false,
					timestamp: new Date()
				}
			];
		} finally {
			isLoading = false;

			setTimeout(() => {
				if (chatContainer) {
					chatContainer.scrollTop = chatContainer.scrollHeight;
				}
			}, 100);
		}
	}

	// Minimal, safe inline Markdown renderer (bold/italic/code/links)
	function escapeHtml(str: string): string {
		return str
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;');
	}

	function escapeAttr(str: string): string {
		return str
			.replace(/&/g, '&amp;')
			.replace(/"/g, '&quot;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;');
	}

	function sanitizeUrl(url: string): string {
		try {
			const u = new URL(url, typeof window !== 'undefined' ? window.location.origin : 'http://localhost');
			const allowed = ['http:', 'https:', 'mailto:', 'tel:'];
			return allowed.includes(u.protocol) ? escapeAttr(u.toString()) : '#';
		} catch {
			return '#';
		}
	}

	function renderInlineMarkdown(text: string): string {
		const escaped = escapeHtml(text);
		// inline code first to avoid inner formatting
		let out = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
		// links: [text](url) — sanitize href and keep label escaped
		out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, label, href) => {
			const safe = sanitizeUrl(href);
			return `<a href="${safe}" target="_blank" rel="noopener noreferrer">${label}</a>`;
		});
		// bold: **text** or __text__
		out = out.replace(/(\*\*|__)(.+?)\1/g, '<strong>$2</strong>');
		// italic: *text* or _text_ (not bold)
		out = out
			.replace(/(^|[^*])\*(?!\*)([^*]+)\*(?!\*)/g, '$1<em>$2</em>')
			.replace(/(^|[^_])_(?!_)([^_]+)_(?!_)/g, '$1<em>$2</em>');
		return out;
	}

	// Block-level renderer with lists and paragraphs
	function renderMarkdown(text: string): string {
		const escapeBasic = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		const inline = (s: string): string => {
			let out = s;
			out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
			out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_m, label, href) => {
				const safe = sanitizeUrl(href);
				return `<a href=\"${safe}\" target=\"_blank\" rel=\"noopener noreferrer\">${label}</a>`;
			});
			out = out.replace(/(\*\*|__)(.+?)\1/g, '<strong>$2</strong>');
			out = out
				.replace(/(^|[^*])\*(?!\*)([^*]+)\*(?!\*)/g, '$1<em>$2</em>')
				.replace(/(^|[^_])_(?!_)([^_]+)_(?!_)/g, '$1<em>$2</em>');
			return out;
		};

		const escaped = escapeBasic(text);
		const lines = escaped.split(/\r?\n/);
		const blocks: string[] = [];
		let i = 0;
		while (i < lines.length) {
			if (lines[i].trim() === '') { i++; continue; }

			if (/^\s*[-*+]\s+/.test(lines[i])) {
				const items: string[] = [];
				while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
					items.push(`<li>${inline(lines[i].replace(/^\s*[-*+]\s+/, ''))}</li>`);
					i++;
				}
				blocks.push(`<ul>${items.join('')}</ul>`);
				continue;
			}

			if (/^\s*\d+\.\s+/.test(lines[i])) {
				const m = lines[i].match(/^\s*(\d+)\.\s+/);
				const start = m ? parseInt(m[1], 10) || 1 : 1;
				const items: string[] = [];
				while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
					items.push(`<li>${inline(lines[i].replace(/^\s*\d+\.\s+/, ''))}</li>`);
					i++;
				}
				blocks.push(`<ol start=\"${start}\">${items.join('')}</ol>`);
				continue;
			}

			const buf: string[] = [];
			while (i < lines.length && lines[i].trim() !== '' && !/^\s*[-*+]\s+/.test(lines[i]) && !/^\s*\d+\.\s+/.test(lines[i])) {
				buf.push(lines[i]);
				i++;
			}
			const paragraph = inline(buf.join('\n')).replace(/\n/g, '<br>');
			blocks.push(`<p>${paragraph}</p>`);
		}

		return blocks.join('\n');
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}
</script>

<div class="chat-container">
	<div class="chat-header">
		<h2>Chat Assistant</h2>
	</div>
	
	<div class="chat-messages" bind:this={chatContainer}>
		{#each messages as message (message.id)}
			<div class="message {message.isUser ? 'user' : 'bot'}">
				<div class="message-content">
					<div class="message-body">{@html renderMarkdown(message.text)}</div>
					<span class="timestamp">
						{message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
					</span>
				</div>
			</div>
		{/each}
		
		{#if isLoading}
			<div class="message bot">
				<div class="message-content">
					<div class="typing-indicator">
						<span></span>
						<span></span>
						<span></span>
					</div>
				</div>
			</div>
		{/if}
	</div>
	
	<div class="chat-input">
		<div class="input-container">
			<textarea
				bind:value={inputMessage}
				on:keydown={handleKeyPress}
				placeholder="Type your message here..."
				rows="1"
				disabled={isLoading}
			></textarea>
			<button on:click={sendMessage} disabled={isLoading || !inputMessage.trim()}>
				Send
			</button>
		</div>
	</div>
</div>

<style>
	.chat-container {
		display: flex;
		flex-direction: column;
		height: calc(100vh - 100px);
		max-width: 800px;
		margin: 0 auto;
		border: 1px solid #ddd;
		border-radius: 8px;
		overflow: hidden;
		background: white;
	}
	
	.chat-header {
		background: #007bff;
		color: white;
		padding: 1rem;
		text-align: center;
	}
	
	.chat-header h2 {
		margin: 0;
	}
	
	.chat-messages {
		flex: 1;
		overflow-y: auto;
		padding: 1rem;
		background: #f8f9fa;
	}
	
	.message {
		margin-bottom: 1rem;
		display: flex;
	}
	
	.message.user {
		justify-content: flex-end;
	}
	
	.message.bot {
		justify-content: flex-start;
	}
	
	.message-content {
		max-width: 70%;
		padding: 0.75rem 1rem;
		border-radius: 18px;
		position: relative;
	}
	
	.message.user .message-content {
		background: #007bff;
		color: white;
	}
	
	.message.bot .message-content {
		background: white;
		border: 1px solid #ddd;
	}
	
	.message-content p {
		margin: 0;
		line-height: 1.4;
		white-space: pre-wrap; /* preserve \n line breaks */
		overflow-wrap: break-word; /* break long words */
		word-break: break-word; /* break long words */
	}

	.message-content ul,
	.message-content ol {
		margin: 0.25rem 0 0.5rem 1.25rem;
		padding: 0;
	}

	.message-content li {
		margin: 0.125rem 0;
	}

	.message-content a {
		color: #0d6efd;
		text-decoration: underline;
		word-break: break-word;
	}
	
	.message-content code {
		background: #f1f3f5;
		padding: 0 0.25rem;
		border-radius: 4px;
		font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
		font-size: 0.9em;
	}

	.timestamp {
		font-size: 0.75rem;
		opacity: 0.7;
		display: block;
		margin-top: 0.25rem;
	}
	
	.typing-indicator {
		display: flex;
		gap: 3px;
		align-items: center;
	}
	
	.typing-indicator span {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #999;
		animation: typing 1.4s infinite ease-in-out;
	}
	
	.typing-indicator span:nth-child(2) {
		animation-delay: 0.2s;
	}
	
	.typing-indicator span:nth-child(3) {
		animation-delay: 0.4s;
	}
	
	@keyframes typing {
		0%, 60%, 100% {
			transform: translateY(0);
		}
		30% {
			transform: translateY(-10px);
		}
	}
	
	.chat-input {
		padding: 1rem;
		background: white;
		border-top: 1px solid #ddd;
	}
	
	.input-container {
		display: flex;
		gap: 0.5rem;
		align-items: flex-end;
	}
	
	textarea {
		flex: 1;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 20px;
		resize: none;
		min-height: 20px;
		max-height: 100px;
		font-family: inherit;
	}
	
	textarea:focus {
		outline: none;
		border-color: #007bff;
	}
	
	button {
		background: #007bff;
		color: white;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 20px;
		cursor: pointer;
		font-weight: 500;
	}
	
	button:hover:not(:disabled) {
		background: #0056b3;
	}
	
	button:disabled {
		background: #ccc;
		cursor: not-allowed;
	}
	
	@media (max-width: 768px) {
		.chat-container {
			height: calc(100vh - 80px);
			border-radius: 0;
			border-left: none;
			border-right: none;
		}
		
		.message-content {
			max-width: 85%;
		}
	}
</style>
