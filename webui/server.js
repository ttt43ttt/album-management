const path = require('path');
const express = require('express');
const proxy = require('http-proxy-middleware');
const webpack = require('webpack');
const signale = require('signale');
const mockApiMiddleware = require('express-mock-api-middleware');
const historyMiddleware = require('connect-history-api-fallback');
const webpackDevMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');

const webpackConfig = require('./webpack.config');
const proxyConfig = require('./server-proxy.config');

// ============= ENVIRONMENT VARIABLES =============
const port = process.env.PORT || 8000;
const host = process.env.HOST || 'localhost';
const apiTarget = process.env.API; // API=mock or http://localhost:8080

const app = express();
const compiler = webpack(webpackConfig);

const historyMiddlewareHandler = historyMiddleware();

const webpackDevMiddlewareHandler = webpackDevMiddleware(compiler, {
  reload: true,
  logLevel: 'warn',
  publicPath: webpackConfig.output.publicPath,
});

const webpackHotMiddlewareHandler = webpackHotMiddleware(compiler);

if (apiTarget === 'mock') {
  // mock api
  app.use(mockApiMiddleware(path.resolve(__dirname, 'mock')));
} else {
  const baseConfig = { changeOrigin: true, headers: { 'User-Agent': '' } };

  proxyConfig.list.forEach(({ apiPath, config }) => {
    app.use(proxy(apiPath, { ...baseConfig, ...config }));
  });
}

app.use(express.static(path.join(__dirname, 'assets')));
app.use(historyMiddlewareHandler);
app.use(webpackDevMiddlewareHandler);
app.use(webpackHotMiddlewareHandler);

app.listen(port, host, error => {
  if (error) {
    signale.error(error);
    return;
  }
  signale.info('Listening on %s. Open http://%s:%s/ in your browser.', port, host, port);
});
