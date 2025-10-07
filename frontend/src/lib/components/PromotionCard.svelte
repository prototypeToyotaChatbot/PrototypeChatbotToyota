<script lang="ts">
	export let data: {
		promotions?: Array<{
			title: string;
			discount_amount?: string | number;
			discount_percentage?: string | number;
			variant_name: string;
			model_name: string;
			original_price: string | number;
			discounted_price?: string | number;
			start_date?: string;
			end_date?: string;
			terms?: string;
		}>;
	};

	function formatPrice(price: string | number): string {
		const numPrice = typeof price === 'string' ? parseFloat(price) : price;
		return new Intl.NumberFormat('id-ID', {
			style: 'currency',
			currency: 'IDR',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(numPrice);
	}

	function formatDate(dateStr: string): string {
		try {
			const date = new Date(dateStr);
			return date.toLocaleDateString('id-ID', {
				day: 'numeric',
				month: 'long',
				year: 'numeric'
			});
		} catch {
			return dateStr;
		}
	}

	function calculateDiscount(original: string | number, discounted: string | number): number {
		const origPrice = typeof original === 'string' ? parseFloat(original) : original;
		const discPrice = typeof discounted === 'string' ? parseFloat(discounted) : discounted;
		return Math.round(((origPrice - discPrice) / origPrice) * 100);
	}
</script>

<div class="promotions">
	{#if data.promotions && data.promotions.length > 0}
		<div class="promo-grid">
			{#each data.promotions as promo}
				<div class="promo-card">
					<div class="promo-badge">
						{#if promo.discount_percentage}
							<span class="discount-badge">-{promo.discount_percentage}%</span>
						{:else if promo.discounted_price}
							<span class="discount-badge">-{calculateDiscount(promo.original_price, promo.discounted_price)}%</span>
						{/if}
					</div>

					<div class="promo-header">
						<h3>{promo.title}</h3>
					</div>

					<div class="promo-details">
						<div class="car-info">
							<h4>{promo.model_name}</h4>
							<p class="variant">{promo.variant_name}</p>
						</div>

						<div class="price-section">
							<div class="original-price">{formatPrice(promo.original_price)}</div>
							{#if promo.discounted_price}
								<div class="discounted-price">{formatPrice(promo.discounted_price)}</div>
							{:else if promo.discount_amount}
								<div class="discount-amount">
									Hemat {formatPrice(promo.discount_amount)}
								</div>
							{/if}
						</div>

						{#if promo.start_date && promo.end_date}
							<div class="promo-period">
								<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
									<rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
								<span>{formatDate(promo.start_date)} - {formatDate(promo.end_date)}</span>
							</div>
						{/if}

						{#if promo.terms}
							<div class="terms">
								<details>
									<summary>Syarat & Ketentuan</summary>
									<p>{promo.terms}</p>
								</details>
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<div class="no-promo">
			<p>Tidak ada promo tersedia saat ini.</p>
		</div>
	{/if}
</div>

<style>
	.promotions {
		margin-top: 0.5rem;
	}

	.promo-grid {
		display: grid;
		gap: 0.875rem;
		grid-template-columns: 1fr;
	}

	.promo-card {
		background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
		border-radius: 12px;
		overflow: hidden;
		border: 2px solid #ffcccc;
		position: relative;
		transition: all 0.3s ease;
	}

	.promo-card:hover {
		box-shadow: 0 6px 16px rgba(204, 0, 0, 0.15);
		border-color: #CC0000;
		transform: translateY(-2px);
	}

	.promo-badge {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		z-index: 1;
	}

	.discount-badge {
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		padding: 0.375rem 0.75rem;
		border-radius: 20px;
		font-weight: 700;
		font-size: 0.875rem;
		box-shadow: 0 2px 8px rgba(204, 0, 0, 0.3);
	}

	.promo-header {
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		padding: 1rem;
		border-bottom: 1px solid #ffcccc;
	}

	.promo-header h3 {
		margin: 0;
		color: #CC0000;
		font-size: 1.0625rem;
		font-weight: 700;
		line-height: 1.3;
	}

	.promo-details {
		padding: 1rem;
	}

	.car-info h4 {
		margin: 0 0 0.25rem 0;
		color: #222;
		font-size: 1rem;
		font-weight: 700;
	}

	.variant {
		margin: 0 0 0.875rem 0;
		color: #666;
		font-size: 0.875rem;
	}

	.price-section {
		margin-bottom: 0.875rem;
	}

	.original-price {
		color: #999;
		font-size: 0.875rem;
		text-decoration: line-through;
		margin-bottom: 0.25rem;
	}

	.discounted-price {
		color: #CC0000;
		font-size: 1.25rem;
		font-weight: 700;
	}

	.discount-amount {
		color: #CC0000;
		font-size: 1rem;
		font-weight: 700;
	}

	.promo-period {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: #666;
		font-size: 0.8125rem;
		margin-bottom: 0.75rem;
		padding: 0.5rem;
		background: #f5f5f5;
		border-radius: 8px;
	}

	.promo-period svg {
		flex-shrink: 0;
		color: #CC0000;
	}

	.terms {
		margin-top: 0.75rem;
	}

	.terms details {
		background: #f9f9f9;
		border-radius: 8px;
		padding: 0.625rem;
		border: 1px solid #e8e8e8;
	}

	.terms summary {
		color: #CC0000;
		font-size: 0.8125rem;
		font-weight: 600;
		cursor: pointer;
		user-select: none;
	}

	.terms summary:hover {
		opacity: 0.8;
	}

	.terms p {
		margin: 0.625rem 0 0 0;
		color: #555;
		font-size: 0.8125rem;
		line-height: 1.5;
	}

	.no-promo {
		text-align: center;
		padding: 2rem 1rem;
		color: #999;
	}

	.no-promo p {
		margin: 0;
		font-size: 0.9375rem;
	}

	@media (max-width: 480px) {
		.promo-header h3 {
			font-size: 1rem;
		}

		.car-info h4 {
			font-size: 0.9375rem;
		}

		.discounted-price {
			font-size: 1.125rem;
		}
	}
</style>
