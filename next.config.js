/** @type {import('next').NextConfig} */
const isGithubPages = process.env.GITHUB_PAGES === 'true';
const repositoryName = 'LangChain_Enterprise_Dashboard';

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: isGithubPages ? 'export' : undefined,
  basePath: isGithubPages ? `/${repositoryName}` : '',
  assetPrefix: isGithubPages ? `/${repositoryName}` : '',
  images: {
    unoptimized: isGithubPages,
  },
  experimental: {
    optimizePackageImports: ['recharts', 'lucide-react'],
  },
};

module.exports = nextConfig;

