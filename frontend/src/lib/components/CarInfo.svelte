<script lang="ts">
	export let data: {
		car?: {
			model_name: string;
			variant_name?: string;
			price: string | number;
			image_url?: string;
			specs?: {
				engine?: string;
				transmission?: string;
				fuel_type?: string;
				seating_capacity?: number;
			};
			features?: string[];
			benefits?: string[];
			use_cases?: string[];
			catalog_link?: string;
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

{#if data.car}
	<div class="car-info">
		{#if data.car.image_url}
			<div class="car-image">
				<img src={data.car.image_url} alt={data.car.model_name} loading="lazy" />
			</div>
		{/if}

		<div class="car-header">
			<h3>{data.car.model_name}</h3>
			{#if data.car.variant_name}
				<p class="variant">{data.car.variant_name}</p>
			{/if}
			<p class="price">{formatPrice(data.car.price)}</p>
		</div>

		{#if data.car.specs}
			<div class="specs-section">
				<h4>Spesifikasi</h4>
				<div class="spec-grid">
					{#if data.car.specs.engine}
						<div class="spec-item">
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
							<div>
								<span class="spec-label">Mesin</span>
								<span class="spec-value">{data.car.specs.engine}</span>
							</div>
						</div>
					{/if}
					{#if data.car.specs.transmission}
						<div class="spec-item">
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
								<path d="M12 1v6m0 6v10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
							</svg>
							<div>
								<span class="spec-label">Transmisi</span>
								<span class="spec-value">{data.car.specs.transmission}</span>
							</div>
						</div>
					{/if}
					{#if data.car.specs.fuel_type}
						<div class="spec-item">
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M14 11V2H6v9M3 2h15M6 18h8M6 11h8v7H6v-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M14 15h4.5a1.5 1.5 0 001.5-1.5v-3l-3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M4 22h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
							</svg>
							<div>
								<span class="spec-label">Bahan Bakar</span>
								<span class="spec-value">{data.car.specs.fuel_type}</span>
							</div>
						</div>
					{/if}
					{#if data.car.specs.seating_capacity}
						<div class="spec-item">
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<circle cx="8.5" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M20 8v6M23 11h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
							<div>
								<span class="spec-label">Kapasitas</span>
								<span class="spec-value">{data.car.specs.seating_capacity} Penumpang</span>
							</div>
						</div>
					{/if}
				</div>
			</div>
		{/if}

		{#if data.car.features && data.car.features.length > 0}
			<div class="features-section">
				<h4>Fitur Unggulan</h4>
				<ul>
					{#each data.car.features as feature}
						<li>{feature}</li>
					{/each}
				</ul>
			</div>
		{/if}

		{#if data.car.benefits && data.car.benefits.length > 0}
			<div class="benefits-section">
				<h4>Kelebihan</h4>
				<ul>
					{#each data.car.benefits as benefit}
						<li>{benefit}</li>
					{/each}
				</ul>
			</div>
		{/if}

		{#if data.car.use_cases && data.car.use_cases.length > 0}
			<div class="use-cases-section">
				<h4>Cocok Untuk</h4>
				<div class="tags">
					{#each data.car.use_cases as useCase}
						<span class="tag">{useCase}</span>
					{/each}
				</div>
			</div>
		{/if}

		{#if data.car.catalog_link}
			<a href={data.car.catalog_link} target="_blank" rel="noopener noreferrer" class="catalog-link">
				Lihat E-Catalog Lengkap
				<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					<path d="M15 3h6v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					<path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
				</svg>
			</a>
		{/if}
	</div>
{/if}

<style>
	.car-info {
		margin-top: 0.5rem;
		background: #fafafa;
		border-radius: 12px;
		overflow: hidden;
		border: 1px solid #e8e8e8;
	}

	.car-image {
		width: 100%;
		height: 180px;
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

	.car-header {
		padding: 1rem;
		background: white;
		border-bottom: 1px solid #e8e8e8;
	}

	.car-header h3 {
		margin: 0 0 0.25rem 0;
		color: #222;
		font-size: 1.125rem;
		font-weight: 700;
		line-height: 1.3;
	}

	.variant {
		margin: 0 0 0.5rem 0;
		color: #666;
		font-size: 0.875rem;
	}

	.price {
		margin: 0;
		color: #CC0000;
		font-size: 1.25rem;
		font-weight: 700;
	}

	.specs-section,
	.features-section,
	.benefits-section,
	.use-cases-section {
		padding: 1rem;
		background: white;
		margin-top: 1px;
	}

	.specs-section h4,
	.features-section h4,
	.benefits-section h4,
	.use-cases-section h4 {
		margin: 0 0 0.875rem 0;
		color: #333;
		font-size: 0.875rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.025em;
	}

	.spec-grid {
		display: grid;
		gap: 0.75rem;
	}

	.spec-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.75rem;
		background: #f9f9f9;
		border-radius: 10px;
		border: 1px solid #e8e8e8;
	}

	.spec-item svg {
		flex-shrink: 0;
		color: #CC0000;
	}

	.spec-item > div {
		display: flex;
		flex-direction: column;
		gap: 0.125rem;
		flex: 1;
	}

	.spec-label {
		color: #666;
		font-size: 0.75rem;
		font-weight: 500;
	}

	.spec-value {
		color: #222;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.features-section ul,
	.benefits-section ul {
		margin: 0;
		padding-left: 1.25rem;
		color: #555;
	}

	.features-section li,
	.benefits-section li {
		margin-bottom: 0.5rem;
		font-size: 0.875rem;
		line-height: 1.5;
	}

	.features-section li::marker {
		color: #CC0000;
	}

	.benefits-section li::marker {
		color: #00AA00;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.tag {
		display: inline-block;
		padding: 0.375rem 0.75rem;
		background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
		border: 1px solid #ffcccc;
		color: #CC0000;
		border-radius: 16px;
		font-size: 0.8125rem;
		font-weight: 600;
	}

	.catalog-link {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		margin: 1rem;
		padding: 0.75rem 1.25rem;
		background: linear-gradient(135deg, #CC0000 0%, #E60000 100%);
		color: white;
		text-decoration: none;
		border-radius: 10px;
		font-size: 0.9375rem;
		font-weight: 600;
		transition: all 0.2s ease;
		box-shadow: 0 2px 8px rgba(204, 0, 0, 0.25);
	}

	.catalog-link:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(204, 0, 0, 0.35);
	}

	.catalog-link svg {
		width: 16px;
		height: 16px;
	}

	@media (max-width: 480px) {
		.car-image {
			height: 160px;
		}

		.car-header h3 {
			font-size: 1rem;
		}

		.price {
			font-size: 1.125rem;
		}
	}
</style>
