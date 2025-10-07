<script lang="ts">
  import { onMount } from 'svelte';

  onMount(() => {
    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js').catch(() => {
        // Silently fail if service worker is not available
      });
    }
  });
</script>

<svelte:head>
  <title>Toyota Chatbot Assistant</title>
  <meta name="description" content="Asisten virtual Toyota untuk rekomendasi mobil, informasi produk, dan layanan" />
</svelte:head>

<slot />

<style global lang="postcss">
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  :global(html, body) {
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  :global(body) {
    background: #FFFFFF;
    color: #1a1a1a;
  }

  :global(button) {
    font-family: inherit;
    cursor: pointer;
    border: none;
    background: none;
  }

  :global(input, textarea) {
    font-family: inherit;
    border: none;
    outline: none;
  }

  :global(a) {
    color: inherit;
    text-decoration: none;
  }

  :global(::-webkit-scrollbar) {
    width: 6px;
    height: 6px;
  }

  :global(::-webkit-scrollbar-track) {
    background: #f1f1f1;
  }

  :global(::-webkit-scrollbar-thumb) {
    background: #CC0000;
    border-radius: 3px;
  }

  :global(::-webkit-scrollbar-thumb:hover) {
    background: #B00000;
  }
</style>