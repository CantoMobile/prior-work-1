import React from 'react';
import { Link } from 'react-router-dom';
import { NewSiteForm } from '../components/NewSiteForm'

export const AddSite = () => {

  return (
    <div className="add-site">
        <h3 id="add-site-header">Create a Cantonica listing for a mobile web application that you own or love!</h3>
        <NewSiteForm/>
      
    </div>
  );
}
