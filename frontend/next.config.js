/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/mcp/:path*',
        destination: 'http://localhost:8000/mcp/:path*',
      },
    ];
  },
};

module.exports = nextConfig;