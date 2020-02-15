import React from 'react';
import { Router, Route, Redirect, Switch } from 'dva/router';
import Layout from './layouts';
import AllPhotosPage from './pages/AllPhotosPage';

function RouterConfig({ history }) {
  return (
    <Layout>
      <Router history={history}>
        <Switch>
          <Redirect exact from="/" to="/all-photos" />
          <Route path="/all-photos" exact component={AllPhotosPage} />
        </Switch>
      </Router>
    </Layout>
  );
}

export default RouterConfig;
