<div class="app">
	<header>
		<nav>
			<h1>Chatbot PWA</h1>
		</nav>
	</header>

	<main>
		<slot />
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	header {
		background: #f5f5f5;
		border-bottom: 1px solid #ddd;
		padding: 1rem;
	}

	nav {
		display: flex;
		justify-content: center;
		align-items: center;
		max-width: 1200px;
		margin: 0 auto;
	}

	h1 {
		margin: 0;
		color: #333;
	}

	main {
		flex: 1;
		width: 100%;
		max-width: 1200px;
		margin: 0 auto;
		padding: 1rem;
	}

	:global(body) {
		margin: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background: #fafafa;
	}

	:global(*) {
		box-sizing: border-box;
	}
</style>
