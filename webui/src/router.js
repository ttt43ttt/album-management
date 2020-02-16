import React from 'react';
import { Router, Route, Redirect, Switch } from 'dva/router';
import Layout from './layouts';
import AllPhotosPage from './pages/AllPhotosPage';
import PersonsPage from './pages/PersonsPage';
import PersonPhotosPage from './pages/PersonPhotosPage';

function RouterConfig({ history }) {
  return (
    <Router history={history}>
      <Layout>
        <Switch>
          <Redirect exact from="/" to="/all-photos" />
          <Route path="/all-photos" exact component={AllPhotosPage} />
          <Route path="/persons" exact component={PersonsPage} />
          <Route path="/persons/:id" exact component={PersonPhotosPage} />
        </Switch>
      </Layout>
    </Router>
  );
}

export default RouterConfig;
