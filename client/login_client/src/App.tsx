import React from 'react';
import './App.css';

import { SignupFormComponent } from './signup/view/signup_form';

function App(): JSX.Element {
  return (
    <div>
      <SignupFormComponent />
    </div>
  );
}

export { App };
