<script lang="ts">
	export let data: {
		cars?: Array<{
			name: string;
			variant?: string;
			price: string | number;
			features: string[];
			image_url?: string;
			catalog_link?: string;
		}>;
		generation_info?: {
			generation: string;
			characteristics: string[];
		};
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
</script>

<div class="recommendations">
	{#if data.generation_info}
		<div class="generation-info">
			<h4>Profil Anda: {data.generation_info.generation}</h4>
			<ul class="characteristics">
				{#each data.generation_info.characteristics as characteristic}
					<li>{characteristic}</li>
				{/each}
			</ul>
		</div>
	{/if}

	{#if data.cars && data.cars.length > 0}
		<div class="cars-grid">
			{#each data.cars as car, index}
				<div class="car-card">
					<div class="car-number">{index + 1}</div>
					{#if car.image_url}
						<div class="car-image">
							<img src={car.image_url} alt={car.name} loading="lazy" />
						</div>
					{/if}
					<div class="car-details">
						<h3 class="car-name">{car.name}</h3>
						{#if car.variant}
							<p class="car-variant">{car.variant}</p>
						{/if}
						<p class="car-price">{formatPrice(car.price)}</p>
						
						{#if car.features && car.features.length > 0}
							<div class="features">
								<h4>Top 3 Fitur:</h4>
								<ul>
									{#each car.features.slice(0, 3) as feature}
										<li>{feature}</li>
									{/each}
								</ul>
							</div>
						{/if}

						{#if car.catalog_link}
							<a href={car.catalog_link} target="_blank" rel="noopener noreferrer" class="catalog-link">
								Lihat E-Catalog
								<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M15 3h6v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							</a>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.recommendations {
		margin-top: 0.5rem;
	}

	.generation-info {
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		border-radius: 12px;
		padding: 1rem;
		margin-bottom: 1rem;
		border: 1px solid #ffcccc;
	}

	.generation-info h4 {
		margin: 0 0 0.625rem 0;
		color: #CC0000;
		font-size: 0.9375rem;
		font-weight: 600;
	}

	.characteristics {
		margin: 0;
		padding-left: 1.25rem;
		color: #555;
	}

	.characteristics li {
		margin-bottom: 0.375rem;
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.cars-grid {
		display: flex;
		flex-direction: column;
		gap: 0.875rem;
	}

	.car-card {
		background: #fafafa;
		border-radius: 12px;
		overflow: hidden;
		border: 1px solid #e8e8e8;
		position: relative;
		transition: all 0.3s ease;
	}

	.car-card:hover {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		border-color: #CC0000;
	}

	.car-number {
		position: absolute;
		top: 0.75rem;
		left: 0.75rem;
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		width: 32px;
		height: 32px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
		font-size: 0.875rem;
		box-shadow: 0 2px 6px rgba(204, 0, 0, 0.3);
		z-index: 1;
	}

	.car-image {
		width: 100%;
		height: 160px;
		overflow: hidden;
		background: linear-gradient(to bottom, #fff, #f5f5f5);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.car-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.car-details {
		padding: 1rem;
	}

	.car-name {
		margin: 0 0 0.25rem 0;
		color: #222;
		font-size: 1.125rem;
		font-weight: 700;
		line-height: 1.3;
	}

	.car-variant {
		margin: 0 0 0.5rem 0;
		color: #666;
		font-size: 0.875rem;
	}

	.car-price {
		margin: 0 0 0.875rem 0;
		color: #CC0000;
		font-size: 1.125rem;
		font-weight: 700;
	}

	.features {
		margin-top: 0.875rem;
	}

	.features h4 {
		margin: 0 0 0.5rem 0;
		color: #333;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.features ul {
		margin: 0;
		padding-left: 1.25rem;
		color: #555;
	}

	.features li {
		margin-bottom: 0.375rem;
		font-size: 0.8125rem;
		line-height: 1.4;
	}

	.catalog-link {
		display: inline-flex;
		align-items: center;
		gap: 0.375rem;
		margin-top: 0.875rem;
		padding: 0.5rem 1rem;
		background: white;
		border: 1.5px solid #CC0000;
		color: #CC0000;
		text-decoration: none;
		border-radius: 8px;
		font-size: 0.875rem;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.catalog-link:hover {
		background: #CC0000;
		color: white;
		transform: translateY(-1px);
		box-shadow: 0 3px 8px rgba(204, 0, 0, 0.2);
	}

	.catalog-link svg {
		width: 14px;
		height: 14px;
	}

	@media (max-width: 480px) {
		.car-image {
			height: 140px;
		}

		.car-name {
			font-size: 1rem;
		}

		.car-price {
			font-size: 1rem;
		}

		.car-details {
			padding: 0.875rem;
		}
	}
</style>
