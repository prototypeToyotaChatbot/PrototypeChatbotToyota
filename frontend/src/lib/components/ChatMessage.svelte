<script lang="ts">
	import CarRecommendation from './CarRecommendation.svelte';
	import CarComparison from './CarComparison.svelte';
	import PromotionCard from './PromotionCard.svelte';
	import CarInfo from './CarInfo.svelte';

	export let message: {
		id: number;
		text: string;
		isUser: boolean;
		timestamp: Date;
		data?: any;
		type?: 'text' | 'car_recommendation' | 'car_comparison' | 'promotion' | 'car_info';
	};
</script>

<div class="message-wrapper {message.isUser ? 'user' : 'bot'}">
	<div class="message {message.isUser ? 'user' : 'bot'}">
		<div class="message-content">
			{#if message.type === 'car_recommendation' && message.data}
				<div class="text-content">
					<p>{message.text}</p>
				</div>
				<CarRecommendation data={message.data} />
			{:else if message.type === 'car_comparison' && message.data}
				<div class="text-content">
					<p>{message.text}</p>
				</div>
				<CarComparison data={message.data} />
			{:else if message.type === 'promotion' && message.data}
				<div class="text-content">
					<p>{message.text}</p>
				</div>
				<PromotionCard data={message.data} />
			{:else if message.type === 'car_info' && message.data}
				<div class="text-content">
					<p>{message.text}</p>
				</div>
				<CarInfo data={message.data} />
			{:else}
				<p>{message.text}</p>
			{/if}
			<span class="timestamp">
				{message.timestamp.toLocaleTimeString('id-ID', {hour: '2-digit', minute:'2-digit'})}
			</span>
		</div>
	</div>
</div>

<style>
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

	.message-wrapper.user {
		justify-content: flex-end;
	}

	.message-wrapper.bot {
		justify-content: flex-start;
	}
	
	.message {
		display: flex;
		max-width: 85%;
	}

	.message.user {
		justify-content: flex-end;
	}
	
	.message.bot {
		justify-content: flex-start;
	}
	
	.message-content {
		padding: 0.875rem 1.125rem;
		border-radius: 18px;
		position: relative;
		word-wrap: break-word;
		overflow-wrap: break-word;
	}
	
	.message.user .message-content {
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		border-radius: 18px 18px 4px 18px;
		box-shadow: 0 2px 8px rgba(204, 0, 0, 0.2);
	}
	
	.message.bot .message-content {
		background: white;
		border: 1px solid #e8e8e8;
		border-radius: 18px 18px 18px 4px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
		color: #333;
	}
	
	.message-content p {
		margin: 0;
		line-height: 1.5;
		font-size: 0.9375rem;
		white-space: pre-wrap;
	}

	.text-content {
		margin-bottom: 0.75rem;
	}

	.text-content p {
		margin: 0;
		line-height: 1.5;
		font-size: 0.9375rem;
	}
	
	.timestamp {
		font-size: 0.6875rem;
		opacity: 0.65;
		display: block;
		margin-top: 0.375rem;
		text-align: right;
		font-weight: 400;
	}

	.message.user .timestamp {
		color: rgba(255, 255, 255, 0.85);
	}

	.message.bot .timestamp {
		color: #666;
	}

	@media (min-width: 768px) {
		.message {
			max-width: 75%;
		}
	}

	@media (max-width: 480px) {
		.message {
			max-width: 90%;
		}

		.message-content {
			padding: 0.75rem 1rem;
		}

		.message-content p {
			font-size: 0.875rem;
		}
	}
</style>
