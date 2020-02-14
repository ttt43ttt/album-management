const appName = process.env.ENV_APP_NAME || 'app';

const serviceApi = process.env.API || 'http://localhost:10080';

const proxyConfig = {
  list: [{ apiPath: '/api', config: { target: serviceApi } }],
};

switch (appName) {
  case 'anotherApp':
    proxyConfig.list = [
      // { apiPath: '/api/manager/tenant/register', config: { target: adminApi } },
      // { apiPath: '/api/kaptcha/refresh', config: { target: adminApi } },
      // { apiPath: '/api/sms/send-code', config: { target: adminApi } },
      { apiPath: '/api', config: { target: serviceApi } },
    ];
    break;

  default:
    break;
}

module.exports = proxyConfig;
