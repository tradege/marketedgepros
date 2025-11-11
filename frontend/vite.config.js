import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import viteCompression from 'vite-plugin-compression';

export default defineConfig({
  plugins: [
    react(),
    // Gzip compression
    viteCompression({
      algorithm: 'gzip',
      ext: '.gz',
      threshold: 1024, // Only compress files > 1KB
      deleteOriginFile: false,
    }),
    // Brotli compression (better than gzip!)
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
      threshold: 1024,
      deleteOriginFile: false,
    }),
  ],
  envDir: '.',
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info', 'console.debug'], // Remove specific console methods
      },
    },
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // React vendor chunk
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom') || id.includes('node_modules/react-router')) {
            return 'react-vendor';
          }
          
          // Chart libraries (AnalyticsDashboard is 350KB!)
          if (id.includes('node_modules/recharts') || id.includes('node_modules/chart')) {
            return 'charts';
          }
          
          // Utilities
          if (id.includes('node_modules/axios') || id.includes('node_modules/zustand')) {
            return 'utils';
          }
          
          // Icons
          if (id.includes('node_modules/lucide-react')) {
            return 'icons';
          }
          
          // Admin pages (lazy load)
          if (id.includes('/pages/admin/')) {
            return 'admin';
          }
          
          // Other node_modules
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        },
        // Optimize chunk names
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
    chunkSizeWarningLimit: 500, // Warn if chunk > 500KB
    cssCodeSplit: true, // Split CSS into separate files
    sourcemap: false, // Disable sourcemaps in production
    reportCompressedSize: false, // Faster builds
  },
  server: {
    host: true,
    port: 5173
  },
  preview: {
    host: true,
    port: 3000
  }
});
