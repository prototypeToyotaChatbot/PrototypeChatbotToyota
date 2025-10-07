<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let suggestions: string[] = [
		'Rekomendasi mobil keluarga',
		'Promo terbaru',
		'Bandingkan Avanza vs Veloz',
		'Info mobil hybrid'
	];

	const dispatch = createEventDispatcher<{ select: string }>();

	function handleSuggestionClick(suggestion: string) {
		dispatch('select', suggestion);
	}
</script>

<div class="suggestions-container">
	<p class="suggestions-title">Coba tanyakan:</p>
	<div class="suggestions">
		{#each suggestions as suggestion}
			<button
				class="suggestion-chip"
				on:click={() => handleSuggestionClick(suggestion)}
				type="button"
			>
				{suggestion}
			</button>
		{/each}
	</div>
</div>

<style>
	.suggestions-container {
		margin: 1rem 0;
		animation: fadeIn 0.4s ease-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.suggestions-title {
		margin: 0 0 0.75rem 0;
		font-size: 0.875rem;
		color: #666;
		font-weight: 500;
	}

	.suggestions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.suggestion-chip {
		display: inline-flex;
		align-items: center;
		padding: 0.5rem 1rem;
		background: white;
		border: 1.5px solid #e8e8e8;
		color: #333;
		border-radius: 20px;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
		white-space: nowrap;
	}

	.suggestion-chip:hover {
		border-color: #CC0000;
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		color: #CC0000;
		transform: translateY(-1px);
		box-shadow: 0 2px 6px rgba(204, 0, 0, 0.15);
	}

	.suggestion-chip:active {
		transform: translateY(0);
		box-shadow: 0 1px 3px rgba(204, 0, 0, 0.2);
	}

	@media (max-width: 480px) {
		.suggestion-chip {
			font-size: 0.8125rem;
			padding: 0.4375rem 0.875rem;
		}

		.suggestions-title {
			font-size: 0.8125rem;
		}
	}
</style>
