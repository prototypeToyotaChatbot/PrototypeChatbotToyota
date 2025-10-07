<script lang="ts">
	import { onMount } from 'svelte';
	import ChatMessage from '$lib/components/ChatMessage.svelte';
	import QuickSuggestions from '$lib/components/QuickSuggestions.svelte';
	import type { Message, ChatResponse } from '$lib/types';
	import { generateId } from '$lib/utils';

	let messages: Message[] = [];
	let inputMessage = '';
	let isLoading = false;
	let chatContainer: HTMLDivElement;
	let sessionId = generateId();
	let sessionStartedAt = new Date().toISOString();
	let showSuggestions = true;

	const quickSuggestions = [
		'Rekomendasi mobil keluarga budget 300 juta',
		'Promo mobil terbaru',
		'Bandingkan Avanza dan Veloz',
		'Info mobil hybrid Toyota',
		'Cek indent mobil di Jakarta'
	];

	onMount(() => {
		if (typeof window !== 'undefined') {
			sessionId = generateId();
			sessionStartedAt = new Date().toISOString();
		}

		messages = [
			{
				id: Date.now(),
				text: "Halo! Saya asisten Toyota Anda. Saya dapat membantu Anda menemukan mobil yang tepat, membandingkan model, cek promo, dan memberikan rekomendasi berdasarkan kebutuhan Anda. Ada yang bisa saya bantu?",
				isUser: false,
				timestamp: new Date(),
				type: 'text'
			}
		];
	});

	async function sendMessage() {
		if (!inputMessage.trim() || isLoading) return;

		showSuggestions = false;
		const userMessage = inputMessage.trim();
		inputMessage = '';

		messages = [
			...messages,
			{
				id: Date.now(),
				text: userMessage,
				isUser: true,
				timestamp: new Date(),
				type: 'text'
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
			let responseData: any = null;
			let messageType: 'text' | 'car_recommendation' | 'car_comparison' | 'promotion' | 'car_info' = 'text';

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
				botResponse = extractOutput(payload) ?? 'Pesan Anda diterima: ' + userMessage;
				
				// Check if response contains structured data
				if (payload.data) {
					responseData = payload.data;
					if (payload.data.type) {
						messageType = payload.data.type;
					}
				}
			} else {
				botResponse = extractOutput(payload) ?? "Maaf, saya sedang mengalami kendala. Silakan coba lagi nanti.";
			}

			messages = [
				...messages,
				{
					id: Date.now() + 1,
					text: botResponse,
					isUser: false,
					timestamp: new Date(),
					data: responseData,
					type: messageType
				}
			];
		} catch (error) {
			console.error('Error sending message:', error);
			messages = [
				...messages,
				{
					id: Date.now() + 1,
					text: "Maaf, saya sedang mengalami kendala koneksi. Silakan coba lagi nanti.",
					isUser: false,
					timestamp: new Date(),
					type: 'text'
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

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function autoResize(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		target.style.height = 'auto';
		target.style.height = target.scrollHeight + 'px';
	}

	function handleSuggestionSelect(event: CustomEvent<string>) {
		inputMessage = event.detail;
		sendMessage();
	}
</script>

<svelte:head>
	<title>Toyota Chatbot Assistant</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
</svelte:head>

<div class="app-container">
	<div class="chat-container">
		<div class="chat-header">
			<div class="header-content">
				<div class="logo-section">
					<div class="logo-circle">T</div>
					<div class="header-text">
						<h1>Toyota Assistant</h1>
						<p class="subtitle">Siap membantu Anda</p>
					</div>
				</div>
			</div>
		</div>
		
		<div class="chat-messages" bind:this={chatContainer}>
			{#each messages as message (message.id)}
				<ChatMessage {message} />
			{/each}

			{#if showSuggestions && messages.length === 1}
				<QuickSuggestions suggestions={quickSuggestions} on:select={handleSuggestionSelect} />
			{/if}
			
			{#if isLoading}
				<div class="message-wrapper bot">
					<div class="message bot">
						<div class="message-content">
							<div class="typing-indicator">
								<span></span>
								<span></span>
								<span></span>
							</div>
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
					on:input={autoResize}
					placeholder="Ketik pesan Anda di sini..."
					rows="1"
					disabled={isLoading}
				></textarea>
				<button 
					class="send-button" 
					on:click={sendMessage} 
					disabled={isLoading || !inputMessage.trim()}
					aria-label="Kirim pesan"
				>
					<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
			'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
			sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		background: #f5f5f5;
	}

	.app-container {
		width: 100%;
		height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 0;
		background: linear-gradient(135deg, #fef5f5 0%, #fff 100%);
	}

	.chat-container {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		max-width: 100%;
		background: white;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
		overflow: hidden;
	}
	
	.chat-header {
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		padding: 1rem 1.25rem;
		box-shadow: 0 2px 10px rgba(204, 0, 0, 0.15);
		position: sticky;
		top: 0;
		z-index: 10;
	}

	.header-content {
		max-width: 1200px;
		margin: 0 auto;
	}

	.logo-section {
		display: flex;
		align-items: center;
		gap: 0.875rem;
	}

	.logo-circle {
		width: 42px;
		height: 42px;
		border-radius: 50%;
		background: white;
		color: #CC0000;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		font-size: 1.25rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.header-text h1 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		letter-spacing: -0.01em;
	}

	.subtitle {
		margin: 0;
		font-size: 0.8125rem;
		opacity: 0.95;
		font-weight: 400;
	}
	
	.chat-messages {
		flex: 1;
		overflow-y: auto;
		padding: 1.25rem;
		background: #fafafa;
		scroll-behavior: smooth;
	}

	.chat-messages::-webkit-scrollbar {
		width: 6px;
	}

	.chat-messages::-webkit-scrollbar-track {
		background: transparent;
	}

	.chat-messages::-webkit-scrollbar-thumb {
		background: #ddd;
		border-radius: 3px;
	}

	.chat-messages::-webkit-scrollbar-thumb:hover {
		background: #ccc;
	}

	.message-wrapper {
		margin-bottom: 1rem;
		display: flex;
		animation: slideIn 0.3s ease-out;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.message-wrapper.bot {
		justify-content: flex-start;
	}
	
	.message {
		display: flex;
	}
	
	.message.bot {
		justify-content: flex-start;
	}
	
	.message-content {
		padding: 0.75rem 1rem;
		border-radius: 16px;
		position: relative;
	}
	
	.message.bot .message-content {
		background: white;
		border: 1px solid #e8e8e8;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
	}
	
	.typing-indicator {
		display: flex;
		gap: 4px;
		align-items: center;
		padding: 4px 0;
	}
	
	.typing-indicator span {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #CC0000;
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
			opacity: 0.6;
		}
		30% {
			transform: translateY(-8px);
			opacity: 1;
		}
	}
	
	.chat-input {
		padding: 1rem 1.25rem;
		background: white;
		border-top: 1px solid #e8e8e8;
		position: sticky;
		bottom: 0;
	}
	
	.input-container {
		display: flex;
		gap: 0.75rem;
		align-items: flex-end;
		max-width: 1200px;
		margin: 0 auto;
	}
	
	textarea {
		flex: 1;
		padding: 0.875rem 1rem;
		border: 1.5px solid #e0e0e0;
		border-radius: 24px;
		resize: none;
		min-height: 48px;
		max-height: 120px;
		font-family: inherit;
		font-size: 0.9375rem;
		line-height: 1.5;
		transition: all 0.2s ease;
		background: #fafafa;
	}
	
	textarea:focus {
		outline: none;
		border-color: #CC0000;
		background: white;
		box-shadow: 0 0 0 3px rgba(204, 0, 0, 0.08);
	}

	textarea::placeholder {
		color: #999;
	}

	textarea:disabled {
		background: #f5f5f5;
		cursor: not-allowed;
	}
	
	.send-button {
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		border: none;
		width: 48px;
		height: 48px;
		border-radius: 50%;
		cursor: pointer;
		font-weight: 500;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
		box-shadow: 0 2px 8px rgba(204, 0, 0, 0.25);
		flex-shrink: 0;
	}
	
	.send-button:hover:not(:disabled) {
		transform: scale(1.05);
		box-shadow: 0 4px 12px rgba(204, 0, 0, 0.35);
	}

	.send-button:active:not(:disabled) {
		transform: scale(0.95);
	}
	
	.send-button:disabled {
		background: #e0e0e0;
		cursor: not-allowed;
		box-shadow: none;
		color: #999;
	}

	/* Desktop styles */
	@media (min-width: 768px) {
		.app-container {
			padding: 1.5rem;
		}

		.chat-container {
			max-width: 900px;
			height: calc(100vh - 3rem);
			border-radius: 16px;
		}

		.chat-header {
			border-radius: 16px 16px 0 0;
		}
	}
	
	@media (max-width: 767px) {
		.chat-container {
			border-radius: 0;
		}
		
		.chat-header {
			padding: 0.875rem 1rem;
		}

		.logo-circle {
			width: 38px;
			height: 38px;
			font-size: 1.125rem;
		}

		.header-text h1 {
			font-size: 1.125rem;
		}

		.subtitle {
			font-size: 0.75rem;
		}

		.chat-messages {
			padding: 1rem;
		}

		.chat-input {
			padding: 0.875rem 1rem;
		}

		textarea {
			font-size: 16px; /* Prevents zoom on iOS */
		}
	}

	/* Improved mobile touch targets */
	@media (max-width: 480px) {
		.send-button {
			width: 44px;
			height: 44px;
		}
	}
</style>