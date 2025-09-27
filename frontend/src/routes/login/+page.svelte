<script lang="ts">
	import { goto } from '$app/navigation';
	
	let email = '';
	let password = '';
	let isLoading = false;
	let error = '';
	
	async function handleLogin(event: Event) {
		event.preventDefault();
		if (!email || !password) {
			error = 'Please fill in all fields';
			return;
		}
		
		isLoading = true;
		error = '';
		
		try {
			const response = await fetch('/api/auth/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ email, password })
			});
			
			const data = await response.json();
			
			if (response.ok) {
				// Store auth token
				localStorage.setItem('auth_token', data.token);
				// Redirect to main chat page
				goto('/');
			} else {
				error = data.message || 'Login failed. Please try again.';
			}
		} catch (err) {
			console.error('Login error:', err);
			error = 'Network error. Please check your connection.';
		} finally {
			isLoading = false;
		}
	}
	
	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleLogin(event);
		}
	}
</script>

<div class="login-container">
	<div class="login-form">
		<h1>Login</h1>
		<p class="subtitle">Welcome back! Please sign in to your account.</p>
		
		{#if error}
			<div class="error-message">
				{error}
			</div>
		{/if}
		
		<form on:submit={handleLogin}>
			<div class="input-group">
				<label for="email">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					on:keydown={handleKeyPress}
					placeholder="Enter your email"
					disabled={isLoading}
					required
				/>
			</div>
			
			<div class="input-group">
				<label for="password">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					on:keydown={handleKeyPress}
					placeholder="Enter your password"
					disabled={isLoading}
					required
				/>
			</div>
			
			<button type="submit" disabled={isLoading}>
				{isLoading ? 'Signing in...' : 'Sign In'}
			</button>
		</form>
		
		<div class="signup-link">
			<p>Don't have an account? <a href="/register">Sign up here</a></p>
		</div>
	</div>
</div>

<style>
	.login-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: calc(100vh - 2rem);
		padding: 1rem;
	}
	
	.login-form {
		background: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		width: 100%;
		max-width: 400px;
	}
	
	h1 {
		text-align: center;
		margin-bottom: 0.5rem;
		color: #333;
	}
	
	.subtitle {
		text-align: center;
		color: #666;
		margin-bottom: 2rem;
	}
	
	.input-group {
		margin-bottom: 1.5rem;
	}
	
	label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
		color: #333;
	}
	
	input {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
		transition: border-color 0.2s;
	}
	
	input:focus {
		outline: none;
		border-color: #007bff;
	}
	
	input:disabled {
		background: #f5f5f5;
		cursor: not-allowed;
	}
	
	button {
		width: 100%;
		background: #007bff;
		color: white;
		border: none;
		padding: 0.75rem;
		border-radius: 4px;
		font-size: 1rem;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s;
	}
	
	button:hover:not(:disabled) {
		background: #0056b3;
	}
	
	button:disabled {
		background: #ccc;
		cursor: not-allowed;
	}
	
	.error-message {
		background: #ffe6e6;
		color: #d32f2f;
		padding: 0.75rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		text-align: center;
	}
	
	.signup-link {
		text-align: center;
		margin-top: 2rem;
		padding-top: 1rem;
		border-top: 1px solid #eee;
	}
	
	.signup-link p {
		margin: 0;
		color: #666;
	}
	
	.signup-link a {
		color: #007bff;
		text-decoration: none;
	}
	
	.signup-link a:hover {
		text-decoration: underline;
	}
</style>