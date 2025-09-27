<script lang="ts">
	import { goto } from '$app/navigation';
	
	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let isLoading = false;
	let error = '';
	let success = '';
	
	async function handleRegister(event: Event) {
		event.preventDefault();
		
		if (!name || !email || !password || !confirmPassword) {
			error = 'Please fill in all fields';
			return;
		}
		
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}
		
		if (password.length < 6) {
			error = 'Password must be at least 6 characters long';
			return;
		}
		
		isLoading = true;
		error = '';
		success = '';
		
		try {
			const response = await fetch('/api/auth/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ name, email, password })
			});
			
			const data = await response.json();
			
			if (response.ok) {
				success = 'Account created successfully! Redirecting to login...';
				setTimeout(() => {
					goto('/login');
				}, 2000);
			} else {
				error = data.message || 'Registration failed. Please try again.';
			}
		} catch (err) {
			console.error('Registration error:', err);
			error = 'Network error. Please check your connection.';
		} finally {
			isLoading = false;
		}
	}
	
	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleRegister(event);
		}
	}
</script>

<div class="register-container">
	<div class="register-form">
		<h1>Create Account</h1>
		<p class="subtitle">Join us today! Please fill in your details to get started.</p>
		
		{#if error}
			<div class="error-message">
				{error}
			</div>
		{/if}
		
		{#if success}
			<div class="success-message">
				{success}
			</div>
		{/if}
		
		<form on:submit={handleRegister}>
			<div class="input-group">
				<label for="name">Full Name</label>
				<input
					id="name"
					type="text"
					bind:value={name}
					on:keydown={handleKeyPress}
					placeholder="Enter your full name"
					disabled={isLoading}
					required
				/>
			</div>
			
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
					placeholder="Enter your password (min. 6 characters)"
					disabled={isLoading}
					required
				/>
			</div>
			
			<div class="input-group">
				<label for="confirmPassword">Confirm Password</label>
				<input
					id="confirmPassword"
					type="password"
					bind:value={confirmPassword}
					on:keydown={handleKeyPress}
					placeholder="Confirm your password"
					disabled={isLoading}
					required
				/>
			</div>
			
			<button type="submit" disabled={isLoading}>
				{isLoading ? 'Creating Account...' : 'Create Account'}
			</button>
		</form>
		
		<div class="login-link">
			<p>Already have an account? <a href="/login">Sign in here</a></p>
		</div>
	</div>
</div>

<style>
	.register-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: calc(100vh - 2rem);
		padding: 1rem;
	}
	
	.register-form {
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
		background: #28a745;
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
		background: #218838;
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
	
	.success-message {
		background: #e8f5e8;
		color: #2e7d32;
		padding: 0.75rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		text-align: center;
	}
	
	.login-link {
		text-align: center;
		margin-top: 2rem;
		padding-top: 1rem;
		border-top: 1px solid #eee;
	}
	
	.login-link p {
		margin: 0;
		color: #666;
	}
	
	.login-link a {
		color: #007bff;
		text-decoration: none;
	}
	
	.login-link a:hover {
		text-decoration: underline;
	}
</style>