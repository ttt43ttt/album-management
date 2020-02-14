import React from 'react';
import JiraFavorites from '@/components/JiraFavorites';

class Page extends React.Component {
  render() {
    return (
      <div>
        <h2>Jira Favorites</h2>
        <JiraFavorites />
      </div>
    );
  }
}

export default Page;
