import dva from 'dva';
import { message } from 'antd';
import createLoading from 'dva-loading';
import { createHashHistory } from 'history';

import { _setHistory } from '@/utils/router';

import '../theme/index.less';
import './index.less';

import router from './router';
import models from './models';

const history = createHashHistory();
_setHistory(history);

// 1. Initialize
const app = dva({
  history,
  onError(e) {
    message.error(e.message, /* duration */ 3);
  },
});
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
