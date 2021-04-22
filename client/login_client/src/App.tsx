import React from 'react';
import './App.css';

function App(): JSX.Element {
  return (
    <div>
      <div className="create-account-form">
        <div className="create-form-title">{"Get started as a user!"}</div>
        <div className="input-row">
          <input
            className="first-name" 
            type="text" 
            placeholder="First name"
          >
          </input>
          <input 
            className="last-name"
            type="text" 
            placeholder="Last name"
          >
          </input>
        </div>
        <div className="input-row">
          <input
            type="text" 
            placeholder="Business email address"
          >
          </input>
        </div>
        <div className="input-row">
          <input
            type="text"
            placeholder="Create password"
          >
          </input>
        </div>
        <div className="input-row">
          <input
            type="text"
            placeholder="Confirm password"
          >
          </input>
        </div>

        <div className="create-account">
          <button>{"Create Account"}</button>
        </div>
      </div>
    </div>
  );
}

export { App };
