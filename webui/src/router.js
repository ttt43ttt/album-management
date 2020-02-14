import React from 'react';
import { Router, Route, Switch } from 'dva/router';
import Layout from './layouts';
import IndexPage from './pages/IndexPage';
import JiraPage from './pages/JiraPage';
import GithubPullsPage from './pages/GithubPullsPage';

function RouterConfig({ history }) {
  return (
    <Layout>
      <Router history={history}>
        <Switch>
          <Route path="/" exact component={IndexPage} />
          <Route path="/jira" exact component={JiraPage} />
          <Route path="/github/pulls" exact component={GithubPullsPage} />
        </Switch>
      </Router>
    </Layout>
  );
}

export default RouterConfig;
