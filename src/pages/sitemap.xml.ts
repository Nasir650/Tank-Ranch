import type { APIRoute } from 'astro';

const SITE = 'https://tankandtrench.com';
const PAGES = [
  '/',
  '/check/',
  '/pricing/',
  '/about/',
  '/answer-map/',
  '/methodology/',
  '/results/',
  '/library/',
  '/privacy/',
  '/terms/',
];

export const GET: APIRoute = () => {
  const lastmod = new Date().toISOString().split('T')[0];
  const urls = PAGES.map(
    (path) => `  <url>\n    <loc>${SITE}${path}</loc>\n    <lastmod>${lastmod}</lastmod>\n  </url>`
  ).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
    },
  });
};
