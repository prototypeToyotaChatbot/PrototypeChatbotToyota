<script lang="ts">
	export let message: string;
	export let type: 'error' | 'warning' | 'info' = 'error';
	export let dismissible: boolean = false;

	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	function handleDismiss() {
		dispatch('dismiss');
	}
</script>

<div class="alert alert-{type}" role="alert">
	<div class="alert-icon">
		{#if type === 'error'}
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
				<line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
				<circle cx="12" cy="16" r="0.5" fill="currentColor" stroke="currentColor" stroke-width="1"/>
			</svg>
		{:else if type === 'warning'}
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
				<line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
				<circle cx="12" cy="17" r="0.5" fill="currentColor" stroke="currentColor" stroke-width="1"/>
			</svg>
		{:else}
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
				<path d="M12 16v-4M12 8h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
			</svg>
		{/if}
	</div>
	<div class="alert-message">
		{message}
	</div>
	{#if dismissible}
		<button class="alert-dismiss" on:click={handleDismiss} aria-label="Tutup">
			<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
				<line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
				<line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
			</svg>
		</button>
	{/if}
</div>

<style>
	.alert {
		display: flex;
		align-items: flex-start;
		gap: 0.75rem;
		padding: 0.875rem 1rem;
		border-radius: 10px;
		margin: 0.5rem 0;
		animation: slideIn 0.3s ease-out;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.alert-error {
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		border: 1px solid #ffcccc;
		color: #cc0000;
	}

	.alert-warning {
		background: linear-gradient(135deg, #fffbf0 0%, #fff4d6 100%);
		border: 1px solid #ffe4a3;
		color: #b45309;
	}

	.alert-info {
		background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
		border: 1px solid #bae6fd;
		color: #0369a1;
	}

	.alert-icon {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.alert-message {
		flex: 1;
		font-size: 0.875rem;
		line-height: 1.5;
		font-weight: 500;
	}

	.alert-dismiss {
		flex-shrink: 0;
		background: none;
		border: none;
		padding: 0.25rem;
		cursor: pointer;
		color: currentColor;
		opacity: 0.7;
		transition: opacity 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.alert-dismiss:hover {
		opacity: 1;
	}

	@media (max-width: 480px) {
		.alert {
			padding: 0.75rem 0.875rem;
		}

		.alert-message {
			font-size: 0.8125rem;
		}

		.alert-icon svg {
			width: 18px;
			height: 18px;
		}
	}
</style>
