<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	
	// Check authentication status
	let isAuthenticated = false;
	
	onMount(() => {
		// Check if user is logged in (you can implement your own logic here)
		const token = localStorage.getItem('auth_token');
		isAuthenticated = !!token;
		
		// Redirect to login if not authenticated and not on login/register pages
		if (!isAuthenticated && !$page.url.pathname.includes('/login') && !$page.url.pathname.includes('/register')) {
			goto('/login');
		}
	});
	
	function logout() {
		localStorage.removeItem('auth_token');
		isAuthenticated = false;
		goto('/login');
	}
</script>

<div class="app">
	{#if isAuthenticated && !$page.url.pathname.includes('/login') && !$page.url.pathname.includes('/register')}
		<header>
			<nav>
				<h1>Chatbot PWA</h1>
				<button on:click={logout}>Logout</button>
			</nav>
		</header>
	{/if}
	
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
		justify-content: space-between;
		align-items: center;
		max-width: 1200px;
		margin: 0 auto;
	}
	
	h1 {
		margin: 0;
		color: #333;
	}
	
	button {
		background: #007bff;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
	}
	
	button:hover {
		background: #0056b3;
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
