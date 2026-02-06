/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  allowedHosts: ['.monkeycode-ai.online'],
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        target: process.env.API_URL || 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
