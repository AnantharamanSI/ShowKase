const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  const proxy = createProxyMiddleware({
    target: 'http://localhost:5000',
    changeOrigin: true,
  })

  app.use('/members', proxy);
  app.use('/gen_pdf', proxy);
};