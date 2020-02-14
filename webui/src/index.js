import dva from 'dva';

import createLoading from 'dva-loading';

import '../theme/index.less';
import './index.less';

import router from './router';
import models from './models';

// 1. Initialize
const app = dva();
window.g_app = app;

// 2. Plugins
app.use(createLoading());

// 3. Model
models.forEach(model => app.model(model));

// 4. Router
app.router(router);

// 5. Start
app.start('#root');

// react hot loader
if (module.hot && process.env.DEVELOPMENT) {
  module.hot.accept();
}
