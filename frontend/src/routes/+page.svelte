<script lang="ts">
	import { onMount } from 'svelte';
	
	let messages: Array<{id: number, text: string, isUser: boolean, timestamp: Date}> = [];
	let inputMessage = '';
	let isLoading = false;
	let chatContainer: HTMLDivElement;
	
	onMount(() => {
		// Add welcome message
		messages = [...messages, {
			id: Date.now(),
			text: 'Hello! I\'m your chatbot assistant. How can I help you today?',
			isUser: false,
			timestamp: new Date()
		}];
	});
	
	async function sendMessage() {
		if (!inputMessage.trim() || isLoading) return;
		
		const userMessage = inputMessage.trim();
		inputMessage = '';
		
		// Add user message
		messages = [...messages, {
			id: Date.now(),
			text: userMessage,
			isUser: true,
			timestamp: new Date()
		}];
		
		isLoading = true;
		
		try {
			// Call your backend API here
			// For now, this is a simple echo response
			const response = await fetch('/api/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ message: userMessage })
			});
			
			let botResponse = '';
			if (response.ok) {
				const data = await response.json();
				botResponse = data.response || 'I received your message: ' + userMessage;
			} else {
				botResponse = 'Sorry, I\'m having trouble connecting right now. Please try again later.';
			}
			
			// Add bot response
			messages = [...messages, {
				id: Date.now() + 1,
				text: botResponse,
				isUser: false,
				timestamp: new Date()
			}];
		} catch (error) {
			console.error('Error sending message:', error);
			messages = [...messages, {
				id: Date.now() + 1,
				text: 'Sorry, I\'m having trouble connecting right now. Please try again later.',
				isUser: false,
				timestamp: new Date()
			}];
		} finally {
			isLoading = false;
			
			// Scroll to bottom
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
</script>

<div class="chat-container">
	<div class="chat-header">
		<h2>Chat Assistant</h2>
	</div>
	
	<div class="chat-messages" bind:this={chatContainer}>
		{#each messages as message (message.id)}
			<div class="message {message.isUser ? 'user' : 'bot'}">
				<div class="message-content">
					<p>{message.text}</p>
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
