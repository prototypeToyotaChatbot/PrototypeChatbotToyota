<script lang="ts">
	export let data: {
		cars?: Array<{
			name: string;
			variant?: string;
			price: string | number;
			specs?: {
				engine?: string;
				transmission?: string;
				fuel_type?: string;
				seating_capacity?: number;
			};
			features?: {
				safety?: string[];
				comfort?: string[];
			};
		}>;
		comparison_points?: string[];
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

<div class="comparison">
	{#if data.comparison_points && data.comparison_points.length > 0}
		<div class="comparison-summary">
			<h4>Poin Perbandingan:</h4>
			<ul>
				{#each data.comparison_points as point}
					<li>{point}</li>
				{/each}
			</ul>
		</div>
	{/if}

	{#if data.cars && data.cars.length > 0}
		<div class="comparison-grid">
			{#each data.cars as car}
				<div class="comparison-card">
					<div class="car-header">
						<h3>{car.name}</h3>
						{#if car.variant}
							<p class="variant">{car.variant}</p>
						{/if}
						<p class="price">{formatPrice(car.price)}</p>
					</div>

					{#if car.specs}
						<div class="specs-section">
							<h4>Spesifikasi</h4>
							<div class="spec-grid">
								{#if car.specs.engine}
									<div class="spec-item">
										<span class="spec-label">Mesin</span>
										<span class="spec-value">{car.specs.engine}</span>
									</div>
								{/if}
								{#if car.specs.transmission}
									<div class="spec-item">
										<span class="spec-label">Transmisi</span>
										<span class="spec-value">{car.specs.transmission}</span>
									</div>
								{/if}
								{#if car.specs.fuel_type}
									<div class="spec-item">
										<span class="spec-label">Bahan Bakar</span>
										<span class="spec-value">{car.specs.fuel_type}</span>
									</div>
								{/if}
								{#if car.specs.seating_capacity}
									<div class="spec-item">
										<span class="spec-label">Kapasitas</span>
										<span class="spec-value">{car.specs.seating_capacity} Penumpang</span>
									</div>
								{/if}
							</div>
						</div>
					{/if}

					{#if car.features}
						{#if car.features.safety && car.features.safety.length > 0}
							<div class="features-section">
								<h4>Fitur Keselamatan</h4>
								<ul>
									{#each car.features.safety as feature}
										<li>{feature}</li>
									{/each}
								</ul>
							</div>
						{/if}

						{#if car.features.comfort && car.features.comfort.length > 0}
							<div class="features-section">
								<h4>Fitur Kenyamanan</h4>
								<ul>
									{#each car.features.comfort as feature}
										<li>{feature}</li>
									{/each}
								</ul>
							</div>
						{/if}
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.comparison {
		margin-top: 0.5rem;
	}

	.comparison-summary {
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		border-radius: 12px;
		padding: 1rem;
		margin-bottom: 1rem;
		border: 1px solid #ffcccc;
	}

	.comparison-summary h4 {
		margin: 0 0 0.625rem 0;
		color: #CC0000;
		font-size: 0.9375rem;
		font-weight: 600;
	}

	.comparison-summary ul {
		margin: 0;
		padding-left: 1.25rem;
		color: #555;
	}

	.comparison-summary li {
		margin-bottom: 0.375rem;
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.comparison-grid {
		display: grid;
		gap: 0.875rem;
		grid-template-columns: 1fr;
	}

	@media (min-width: 640px) {
		.comparison-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.comparison-card {
		background: #fafafa;
		border-radius: 12px;
		overflow: hidden;
		border: 1px solid #e8e8e8;
		transition: all 0.3s ease;
	}

	.comparison-card:hover {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		border-color: #CC0000;
	}

	.car-header {
		background: white;
		padding: 1rem;
		border-bottom: 1px solid #e8e8e8;
	}

	.car-header h3 {
		margin: 0 0 0.25rem 0;
		color: #222;
		font-size: 1.0625rem;
		font-weight: 700;
		line-height: 1.3;
	}

	.variant {
		margin: 0 0 0.5rem 0;
		color: #666;
		font-size: 0.8125rem;
	}

	.price {
		margin: 0;
		color: #CC0000;
		font-size: 1.0625rem;
		font-weight: 700;
	}

	.specs-section,
	.features-section {
		padding: 1rem;
	}

	.specs-section h4,
	.features-section h4 {
		margin: 0 0 0.75rem 0;
		color: #333;
		font-size: 0.875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.025em;
	}

	.spec-grid {
		display: grid;
		gap: 0.625rem;
	}

	.spec-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem 0.75rem;
		background: white;
		border-radius: 8px;
		border: 1px solid #e8e8e8;
	}

	.spec-label {
		color: #666;
		font-size: 0.8125rem;
		font-weight: 500;
	}

	.spec-value {
		color: #222;
		font-size: 0.8125rem;
		font-weight: 600;
		text-align: right;
	}

	.features-section ul {
		margin: 0;
		padding-left: 1.25rem;
		color: #555;
	}

	.features-section li {
		margin-bottom: 0.375rem;
		font-size: 0.8125rem;
		line-height: 1.4;
	}

	.features-section li::marker {
		color: #CC0000;
	}

	@media (max-width: 480px) {
		.car-header h3 {
			font-size: 1rem;
		}

		.price {
			font-size: 1rem;
		}
	}
</style>
