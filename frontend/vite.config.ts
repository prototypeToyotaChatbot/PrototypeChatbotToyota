import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
	plugins: [
		sveltekit(),
		VitePWA({
			registerType: 'autoUpdate',
			workbox: {
				globPatterns: ['**/*.{js,css,html,ico,png,svg,webp}']
			},
			manifest: {
				name: 'Chatbot PWA',
				short_name: 'Chatbot',
				description: 'Simple chatbot Progressive Web App',
				theme_color: '#ffffff',
				background_color: '#ffffff',
				display: 'standalone',
				scope: '/',
				start_url: '/',
				icons: [
					{
						src: 'pwa-192x192.png',
						sizes: '192x192',
						type: 'image/png'
					},
					{
						src: 'pwa-512x512.png',
						sizes: '512x512',
						type: 'image/png'
					}
				]
			}
		})
	],
	server: {
		proxy: {
			'/api': {
				target: 'http://prototypechatbot-gateway-1:2323',
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path
			}
		}
	}
});
